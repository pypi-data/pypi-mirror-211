import uuid
import dash_bootstrap_components as dbc


class CustomCarousel(dbc.Carousel):
    def __init__(self, id_prefix=None, **carousel_props):
        if id_prefix is None:
            card_id = str(uuid.uuid4())
            id_prefix = f"caraosel-{card_id}"

        carousel_props = carousel_props.copy() if carousel_props else {}
        if 'style' not in carousel_props:
            carousel_props['style'] = {
                "width": "100%",
                "height": "100%",
                "background-color": "lightgray",
                "border": "1px solid black",
                "padding": "10px",
                "border-radius": "5px"
            }
        super(CustomCarousel, self).__init__(
            **carousel_props,
            id=f"{id_prefix}-carousel"
        )