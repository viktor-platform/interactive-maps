from viktor import ViktorController
from viktor.parametrization import ViktorParametrization, GeoPointField, Text
from viktor.views import MapPolygon, MapResult, MapPoint, MapView, MapLine, Color


class Parametrization(ViktorParametrization):
    intro = Text("""
# ✈️ Flight Analysis App! 

In this app, you can analyze a flight path and whether it passes through a no-fly zone.

**Select two points** corresponding to the airports of departure and arrival.
    """)

    dep_airport = GeoPointField('Departing Airport')
    arr_airport = GeoPointField('Arriving Airport')


class Controller(ViktorController):
    label = 'My Map App'
    parametrization = Parametrization

    @MapView('Flight Analysis', duration_guess=1)
    def generate_map(self, params, **kwargs):
        features = []

        # Draw no-fly zone

        no_fly_zone = MapPolygon([
            MapPoint(54.814614, -26.785331),
            MapPoint(54.610949, -15.190123),
            MapPoint(50.824269, -15.429211),
            MapPoint(50.864828, -26.741683)],
            color=Color.red(),
            title="No-fly zone",
            description="⛔ This is a no-fly zone. Stay out of this zone!"
        )

        features.append(no_fly_zone)

        # Draw airports

        if params.dep_airport:
            dep_point = MapPoint.from_geo_point(params.dep_airport, icon='triangle', color=Color.blue())
            features.append(dep_point)

        if params.arr_airport:
            arr_point = MapPoint.from_geo_point(params.arr_airport, icon='triangle-down', color=Color.blue())
            features.append(arr_point)

        # Draw flight path

        if params.dep_airport and params.arr_airport:
            flight_path = MapLine(dep_point, arr_point)
            features.append(flight_path)

        return MapResult(features)
