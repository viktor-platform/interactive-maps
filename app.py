import viktor as vkt


class Parametrization(vkt.ViktorParametrization):
    intro = vkt.Text("""
# ✈️ Flight Analysis App! 

In this app, you can analyze a flight path and whether it passes through a no-fly zone.

**Select two points** corresponding to the airports of departure and arrival.
    """)

    dep_airport = vkt.GeoPointField('Departing Airport')
    arr_airport = vkt.GeoPointField('Arriving Airport')


class Controller(vkt.ViktorController):
    label = 'My Map App'
    parametrization = Parametrization

    @vkt.MapView('Flight Analysis', duration_guess=1)
    def generate_map(self, params, **kwargs):
        features = []

        # Draw no-fly zone

        no_fly_zone = vkt.MapPolygon([
            vkt.MapPoint(54.814614, -26.785331),
            vkt.MapPoint(54.610949, -15.190123),
            vkt.MapPoint(50.824269, -15.429211),
            vkt.MapPoint(50.864828, -26.741683)],
            color=vkt.Color.red(),
            title="No-fly zone",
            description="⛔ This is a no-fly zone. Stay out of this zone!"
        )

        features.append(no_fly_zone)

        # Draw airports

        if params.dep_airport:
            dep_point = vkt.MapPoint.from_geo_point(params.dep_airport, icon='triangle', color=vkt.Color.blue())
            features.append(dep_point)

        if params.arr_airport:
            arr_point = vkt.MapPoint.from_geo_point(params.arr_airport, icon='triangle-down', color=vkt.Color.blue())
            features.append(arr_point)

        # Draw flight path

        if params.dep_airport and params.arr_airport:
            flight_path = vkt.MapLine(dep_point, arr_point)
            features.append(flight_path)

        return vkt.MapResult(features)
