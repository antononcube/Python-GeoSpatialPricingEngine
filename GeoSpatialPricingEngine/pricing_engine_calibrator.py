from __future__ import annotations

from collections.abc import Mapping
from math import atan2, isfinite, pi, sqrt
from typing import Any

from .orders import Orders
from .pricing_engine import PricingEngine
from .tiled_region import TiledRegion


class PricingEngineCalibrator:
    def __init__(
        self,
        orders: Orders,
        tiled_region: TiledRegion,
        pricing_engine: PricingEngine,
    ) -> None:
        self._orders = orders
        self._tiled_region = tiled_region
        self._pricing_engine = pricing_engine

    @property
    def orders(self) -> Orders:
        return self._orders

    @orders.setter
    def orders(self, value: Orders) -> None:
        self._orders = value

    @property
    def tiled_region(self) -> TiledRegion:
        return self._tiled_region

    @tiled_region.setter
    def tiled_region(self, value: TiledRegion) -> None:
        self._tiled_region = value

    @property
    def pricing_engine(self) -> PricingEngine:
        return self._pricing_engine

    @pricing_engine.setter
    def pricing_engine(self, value: PricingEngine) -> None:
        self._pricing_engine = value

    def get_orders(self) -> Orders:
        return self.orders

    def set_orders(self, value: Orders) -> None:
        self.orders = value

    def get_tiled_region(self) -> TiledRegion:
        return self.tiled_region

    def set_tiled_region(self, value: TiledRegion) -> None:
        self.tiled_region = value

    def get_pricing_engine(self) -> PricingEngine:
        return self.pricing_engine

    def set_pricing_engine(self, value: PricingEngine) -> None:
        self.pricing_engine = value

    def calibrate(self, **kwargs: Any) -> PricingEngine:
        """Calibrate tile parameters from transportation-trip price observations.

        ``calibration_records`` has the shape produced by
        :meth:`TiledRegion.to_calibration_records`: each record contains a tile
        path, distance, and observed price.  The supplied JSON specification
        determines bounds, equality constraints, and the residual norm.
        """
        spec = kwargs.get("spec", {})
        records = kwargs.get("calibration_records")
        if records is None:
            records = self.tiled_region.to_calibration_records(self.orders)
        if not isinstance(spec, Mapping):
            raise TypeError("spec must be a mapping")

        records = self._training_records(records, spec)
        if not records:
            raise ValueError("Calibration requires at least one training record")

        try:
            from ortools.linear_solver import pywraplp
        except ImportError as error:
            raise ImportError(
                "Calibration requires Google OR-Tools; install the 'ortools' package"
            ) from error

        solver = pywraplp.Solver.CreateSolver("GLOP")
        if solver is None:
            raise RuntimeError("Google OR-Tools GLOP solver is unavailable")

        model_spec = spec.get("model", {})
        calibration_spec = spec.get("calibration", {})
        distance_only = bool(model_spec.get("distance_only_formula", False))
        if distance_only:
            parameters = self._solve_distance_only(
                solver, records, calibration_spec
            )
        else:
            parameters = self._solve_tile_model(
                solver, records, calibration_spec
            )

        self.pricing_engine.parameters = parameters
        return self.pricing_engine

    @classmethod
    def build_from_json(cls, file_path: Any) -> PricingEngine:
        """Build and calibrate a pricing engine using a JSON specification."""
        from .pricing_engine_builder import PricingEngineBuilder

        builder = PricingEngineBuilder.build_from_json(file_path)
        if builder.pricing_engine is None:
            raise RuntimeError("Builder did not create a pricing engine")
        return builder.pricing_engine

    def _solve_distance_only(
        self, solver: Any, records: list[Mapping[str, Any]], spec: Mapping[str, Any]
    ) -> dict[str, Any]:
        bounds = spec.get("parameter_bounds", {})
        variables = {
            name: self._variable(solver, name, bounds.get(name, {}))
            for name in ("k", "n")
        }
        expressions = [
            {variables["k"]: float(record["distance"]), variables["n"]: 1.0}
            for record in records
        ]
        objective_value = self._add_residual_problem(
            solver, expressions, records, spec.get("objective_norm", "l1")
        )
        return {
            "mode": "distance_only",
            "k": variables["k"].solution_value(),
            "n": variables["n"].solution_value(),
            "objective_value": objective_value,
            "objective_norm": spec.get("objective_norm", "l1"),
        }

    def _solve_tile_model(
        self, solver: Any, records: list[Mapping[str, Any]], spec: Mapping[str, Any]
    ) -> dict[str, Any]:
        tile_ids = sorted({str(tile_id) for record in records for tile_id in record["path"]})
        tile_data = self._tile_data()
        bounds = spec.get("parameter_bounds", {})
        directional_spec = spec.get("directional_variables", {})
        directions = list(directional_spec.get("directions", ("N", "S", "E", "W", "NE", "NW", "SE", "SW")))
        names = ("k", "n", "sn", "en", "p", "ev")
        variables = {
            tile_id: {
                name: self._variable(solver, f"{name}[{tile_id}]", bounds.get(name, {}))
                for name in names
            }
            for tile_id in tile_ids
        }
        directional = {
            tile_id: {
                direction: self._variable(solver, f"dir[{tile_id},{direction}]", directional_spec)
                for direction in directions
            }
            for tile_id in tile_ids
        }
        self._add_constant_constraints(solver, variables, spec.get("constraints", {}))

        expressions = []
        for record in records:
            path = [str(tile_id) for tile_id in record["path"]]
            expression: dict[Any, float] = {}
            for index, tile_id in enumerate(path):
                values = tile_data.get(
                    tile_id,
                    {"diameter": 0.0, "population": 0.0, "elevation": 0.0},
                )
                self._add_coefficient(expression, variables[tile_id]["k"], values["diameter"])
                self._add_coefficient(expression, variables[tile_id]["n"], 1.0)
                self._add_coefficient(expression, variables[tile_id]["p"], values["population"])
                self._add_coefficient(expression, variables[tile_id]["ev"], values["elevation"])
                if index == 0:
                    self._add_coefficient(expression, variables[tile_id]["sn"], 1.0)
                if index == len(path) - 1:
                    self._add_coefficient(expression, variables[tile_id]["en"], 1.0)
                if index < len(path) - 1:
                    direction = self._direction(tile_data, tile_id, path[index + 1])
                    if direction in directional[tile_id]:
                        self._add_coefficient(expression, directional[tile_id][direction], 1.0)
            expressions.append(expression)

        objective_value = self._add_residual_problem(
            solver, expressions, records, spec.get("objective_norm", "l1")
        )
        return {
            "mode": "tile",
            "tiles": {
                tile_id: {
                    **{name: variable.solution_value() for name, variable in tile_variables.items()},
                    "directional_variables": {
                        direction: variable.solution_value()
                        for direction, variable in directional[tile_id].items()
                    },
                }
                for tile_id, tile_variables in variables.items()
            },
            "objective_value": objective_value,
            "objective_norm": spec.get("objective_norm", "l1"),
        }

    @staticmethod
    def _variable(solver: Any, name: str, bounds: Mapping[str, Any]) -> Any:
        return solver.NumVar(
            float(bounds.get("min", -solver.infinity())),
            float(bounds.get("max", solver.infinity())),
            name,
        )

    @staticmethod
    def _add_coefficient(expression: dict[Any, float], variable: Any, value: float) -> None:
        expression[variable] = expression.get(variable, 0.0) + float(value)

    @staticmethod
    def _add_constant_constraints(
        solver: Any, variables: Mapping[str, Mapping[str, Any]], constraints: Mapping[str, Any]
    ) -> None:
        tile_ids = list(variables)
        if len(tile_ids) < 2:
            return
        for name in ("k", "n"):
            if constraints.get(f"{name}_constant_across_tiles", False):
                reference = variables[tile_ids[0]][name]
                for tile_id in tile_ids[1:]:
                    constraint = solver.Constraint(0.0, 0.0)
                    constraint.SetCoefficient(variables[tile_id][name], 1.0)
                    constraint.SetCoefficient(reference, -1.0)

    @staticmethod
    def _add_residual_problem(
        solver: Any, expressions: list[Mapping[Any, float]], records: list[Mapping[str, Any]], objective_norm: str
    ) -> float:
        normalized_norm = objective_norm.lower()
        if normalized_norm not in {"l1", "linf"}:
            raise ValueError("calibration.objective_norm must be 'l1' or 'linf'")
        objective = solver.Objective()
        maximum_residual = solver.NumVar(0.0, solver.infinity(), "maximum_residual") if normalized_norm == "linf" else None
        for index, (expression, record) in enumerate(zip(expressions, records, strict=True)):
            positive = solver.NumVar(0.0, solver.infinity(), f"residual_positive[{index}]")
            negative = solver.NumVar(0.0, solver.infinity(), f"residual_negative[{index}]")
            constraint = solver.Constraint(float(record["price"]), float(record["price"]))
            for variable, coefficient in expression.items():
                constraint.SetCoefficient(variable, coefficient)
            constraint.SetCoefficient(positive, 1.0)
            constraint.SetCoefficient(negative, -1.0)
            if maximum_residual is None:
                objective.SetCoefficient(positive, 1.0)
                objective.SetCoefficient(negative, 1.0)
            else:
                for residual in (positive, negative):
                    bound = solver.Constraint(-solver.infinity(), 0.0)
                    bound.SetCoefficient(residual, 1.0)
                    bound.SetCoefficient(maximum_residual, -1.0)
        if maximum_residual is not None:
            objective.SetCoefficient(maximum_residual, 1.0)
        objective.SetMinimization()
        status = solver.Solve()
        if status != solver.OPTIMAL:
            raise RuntimeError(f"Calibration LP did not find an optimal solution (status {status})")
        return objective.Value()

    def _tile_data(self) -> dict[str, dict[str, float]]:
        taxonomy = self.tiled_region.geo_taxonomy
        data = taxonomy.data
        records = data.to_dict(orient="records")
        result = {}
        for record in records:
            normalized = {str(key).lower(): value for key, value in record.items()}
            tile_id = normalized.get("tile_id", normalized.get("tag"))
            if tile_id is None:
                continue
            diameter = taxonomy.tile_diameter
            if diameter is None:
                area = taxonomy.tile_area(str(tile_id))
                diameter = 2.0 * sqrt(area / pi)
            result[str(tile_id)] = {
                "diameter": self._number(diameter, 0.0),
                "population": self._number(normalized.get("population", normalized.get("pop")), 0.0),
                "elevation": self._number(normalized.get("elevation", normalized.get("elev")), 0.0),
                "lat": self._number(normalized.get("center_lat", normalized.get("lat")), 0.0),
                "lon": self._number(normalized.get("center_lon", normalized.get("lon")), 0.0),
            }
        return result

    @staticmethod
    def _number(value: Any, default: float) -> float:
        try:
            number = default if value is None else float(value)
            return number if isfinite(number) else default
        except (TypeError, ValueError):
            return default

    @staticmethod
    def _direction(
            tile_data: Mapping[str, Mapping[str, float]],
            tile_id: str,
            next_tile_id: str ) -> str | None:
        current, following = tile_data.get(tile_id), tile_data.get(next_tile_id)
        if current is None or following is None:
            return None
        delta_lat, delta_lon = following["lat"] - current["lat"], following["lon"] - current["lon"]
        if delta_lat == 0 and delta_lon == 0:
            return None
        angle = atan2(delta_lon, delta_lat) * 180.0 / pi
        return ("N", "NE", "E", "SE", "S", "SW", "W", "NW")[int((angle + 22.5) % 360 // 45)]

    def _training_records(self,
                          records: Mapping[str, Mapping[str, Any]],
                          spec: Mapping[str, Any] ) -> list[Mapping[str, Any]]:
        selected = list(records.values())
        ingest_spec = spec.get("ingest_orders", {})
        if not ingest_spec.get("split_training_testing", False):
            return selected
        column = ingest_spec.get("training_flag_column", "is_training")
        training_ids = {
            str(record["id"])
            for record in self.orders.data.to_dict(orient="records")
            if bool(record.get(column))
        }
        return [record for record in selected if str(record["id"]) in training_ids]
