from dash import html, dcc
import dash_bootstrap_components as dbc
import uuid

"""A Card component.
Component for creating Bootstrap cards. Use in conjunction with CardBody,
CardImg, CardLink, CardHeader and CardFooter. Can also be used in
conjunction with CardColumns, CardDeck, CardGroup for different layout
options.

Keyword arguments:

- children (a list of or a singular dash component, string or number; optional):
The children of this component.

- id (string; optional):
The ID of this component, used to identify dash components in
callbacks. The ID needs to be unique across all of the components
in an app.

- body (boolean; optional):
Apply the `card-body` class to the card, so that there is no need
to also include a CardBody component in the children of this Card.
Default: False.

- className (string; optional):
**DEPRECATED** Use `class_name` instead.  Often used with CSS to
style elements with common properties.

- class_name (string; optional):
Often used with CSS to style elements with common properties.

- color (string; optional):
Card color, options: primary, secondary, success, info, warning,
danger, light, dark or any valid CSS color of your choice (e.g. a
hex code, a decimal code or a CSS color name). Default is light.

- inverse (boolean; optional):
Invert text colours for use with a darker background.

- key (string; optional):
A unique identifier for the component, used to improve performance
by React.js while rendering components See
https://reactjs.org/docs/lists-and-keys.html for more info.

- loading_state (dict; optional):
Object that holds the loading state object coming from
dash-renderer.

`loading_state` is a dict with keys:

- component_name (string; optional):
    Holds the name of the component that is loading.

- is_loading (boolean; optional):
    Determines if the component is loading or not.

- prop_name (string; optional):
    Holds which property is loading.

- outline (boolean; optional):
Apply color styling to just the border of the card.

- style (dict; optional):
Defines CSS styles which will override styles previously set.

- image_src(string; optional):
Defines path of image to be displayed.

- card_text (string; optional)
The text content to be displayed in the body of the card.

- card_title (string; optional)
The title or heading of the card.

- link_label (list; optional)
A list of labels for the links to be displayed in the card. Each label represents a link.

- button_label (list; optional)
A list of labels for the buttons to be displayed in the card. Each label represents a button.

-image_position(string,optional)
The position of the image in the card. Valid options are 'right' or 'left'.

-bullet_points(list,optional)
List of data to be shown in bullet points

- id_prefix (string; optional):
A prefix to be added to the `id` attribute of the elements within the card component.
This can be useful for creating unique and identifiable IDs for the card elements, especially when
multiple instances of the card component are used within the same application.

- button_title(string; optional):
To be used in HomePageCard.

- button_title2(string; optional):
To be used in HomePageCard.
"""

class CalloutCards(dbc.Card):
    def __init__(self, id_prefix=None, **card_props):
        if id_prefix is None:
            card_id = str(uuid.uuid4())
            id_prefix = f"callout-card-{card_id}"

        super(CalloutCards, self).__init__(
            dbc.Card(
                [
                    dbc.CardBody(
                        [
                            html.H4(card_props.get("card_title", "Card Title"), className="card-title", id=f"{id_prefix}-title"),
                            html.P(
                                card_props.get("card_text", "Card Text"), className="card-text", id=f"{id_prefix}-text"
                            ),
                            html.P(
                                [
                                    html.P(
                                        dbc.Button(
                                            link['label'],
                                            outline=True,
                                            color="primary",
                                            className="w-100",
                                            style={"border-radius": "50px"},
                                            href=link['link']
                                        ),
                                        id=f"{id_prefix}-button-{index}"
                                    )
                                    for index, link in enumerate(card_props.get('button_label', []))
                                ]
                            ),
                            html.P(
                                [
                                    html.P(
                                        dbc.CardLink(
                                            link["label"],
                                            href=link["link"],
                                            id=f"{id_prefix}-link-{index}"
                                        )
                                    )
                                    for index, link in enumerate(card_props.get('link_label', []))
                                ]
                            )
                        ]
                    )
                ],
                style={"width": "18rem"} if "style" not in card_props else card_props.get("style"),
                id=f"{id_prefix}-card"
            )
        )


class FeatureCards(dbc.Card):
    def __init__(self, id_prefix=None, **card_props):
        if id_prefix is None:
            card_id = str(uuid.uuid4())
            id_prefix = f"feature-card-{card_id}"

        super(FeatureCards, self).__init__(
            dbc.Card(
                [
                    dbc.Row([
                        dbc.Col(
                            dbc.CardImg(src=card_props.get("image_src", ""), id=f"{id_prefix}-image")
                        ) if card_props.get("image_position") == "left" else None,
                        dbc.Col(
                            dbc.CardBody(
                                [
                                    html.H4(card_props.get("card_title", "Card Title"), className="card-title", id=f"{id_prefix}-title"),
                                    html.P(
                                        card_props.get("card_text", "Card Text"), className="card-text", id=f"{id_prefix}-text"
                                    ),
                                    html.Div(
                                        [
                                            html.P(
                                                dbc.Button(
                                                    link['label'],
                                                    outline=True,
                                                    color="primary",
                                                    className="w-15 mx-1",
                                                    style={"border-radius": "50px"},
                                                    href=link['link'],
                                                    id=f"{id_prefix}-button-{index}"
                                                )
                                            )
                                            for index, link in enumerate(card_props.get('button_label', []))
                                        ]
                                    ),
                                    html.P(
                                        [
                                            html.P(
                                                dbc.CardLink(
                                                    link["label"],
                                                    href=link["link"],
                                                    id=f"{id_prefix}-link-{index}"
                                                )
                                            )
                                            for index, link in enumerate(card_props.get("link_label", []))
                                        ]
                                    )
                                ]
                            )
                        ),
                        dbc.Col(
                            dbc.CardImg(src=card_props.get("image_src", ""), id=f"{id_prefix}-image")
                        ) if card_props.get("image_position") != "left" else None,
                    ])
                ],
                style={"width": "18rem"} if 'style' not in card_props else card_props.get('style'),
                id=f"{id_prefix}-card"
            )
        )


class FeatureCardsTwo(dbc.Card):
    def __init__(self, id_prefix=None, **card_props):
        if id_prefix is None:
            card_id = str(uuid.uuid4())
            id_prefix = f"feature-card-{card_id}"

        super(FeatureCardsTwo, self).__init__(
            dbc.Card(
                [
                    dbc.CardImg(src=card_props.get("image_src", ""), top=True, id=f"{id_prefix}-image"),
                    dbc.CardBody(
                        [
                            html.H4(card_props.get("card_title", "Card Title"), className="card-title", id=f"{id_prefix}-title"),
                            html.P(
                                card_props.get("card_text", "Card Text"), className="card-text", id=f"{id_prefix}-text"
                            ),
                            html.Div(
                                [
                                    html.P(
                                        dbc.Button(
                                            link['label'],
                                            outline=True,
                                            color="primary",
                                            className="w-15 mx-1",
                                            style={"border-radius": "50px"},
                                            href=link['link'],
                                            id=f"{id_prefix}-button-{index}"
                                        )
                                    )
                                    for index, link in enumerate(card_props.get('button_label', []))
                                ]
                            ),
                            html.P(
                                [
                                    html.P(
                                        dbc.CardLink(
                                            link["label"],
                                            href=link["link"],
                                            id=f"{id_prefix}-link-{index}"
                                        )
                                    )
                                    for index, link in enumerate(card_props.get("link_label", []))
                                ]
                            )
                        ]
                    )
                ],
                style={"width": "18rem"} if "style" not in card_props else card_props.get("style"),
                id=f"{id_prefix}-card"
            )
        )


class ImageLeftContentRightCard(dbc.Card):
    def __init__(self, id_prefix=None, **card_props):
        if id_prefix is None:
            card_id = str(uuid.uuid4())
            id_prefix = f"imageleftcontentright-card-{card_id}"

        super(ImageLeftContentRightCard, self).__init__(
            dbc.Card(
                [
                    dbc.Row([
                        dbc.Col(
                            dbc.CardImg(src=card_props.get("image_src", ""), id=f"{id_prefix}-image")
                        ),
                        dbc.Col(
                            [
                                dbc.CardBody(
                                    html.P(card_props.get("card_text", "Card Text"), className="card-text",
                                           id=f"{id_prefix}-text")
                                ) if "card_text" in card_props else None,
                                dbc.CardBody(
                                    [
                                        html.Ul(
                                            [
                                                html.Li(point, id=f"{id_prefix}-point-{index}")
                                                for index, point in enumerate(card_props.get("bullet_points", []))
                                            ],
                                            style={"list-style-type": "disc"}
                                        ) if "bullet_points" in card_props else None
                                    ]
                                )
                            ]
                        )
                    ])
                ],
                style={"width": "18rem"} if 'style' not in card_props else card_props.get('style'),
                id=f"{id_prefix}-card"
            )
        )


class LargeImageCards(dbc.Card):
    def __init__(self, id_prefix=None, **card_props):
        if id_prefix is None:
            card_id = str(uuid.uuid4())
            id_prefix = f"largeimagecards-card-{card_id}"

        super(LargeImageCards, self).__init__(
            dbc.Card(
                [
                    dbc.CardImg(src=card_props.get("image_src", ""), top=True, id=f"{id_prefix}-image-top")
                    if card_props.get("image_position") == "top" else None,
                    dbc.CardBody(
                        [
                            html.H4(card_props.get("card_title", "Card Title"), className="card-title", id=f"{id_prefix}-title"),
                            html.P(
                                card_props.get("card_text", "Card Text"), className="card-text", id=f"{id_prefix}-text",
                            ),
                            html.Div(
                                [
                                    html.P(
                                        dbc.Button(
                                            link['label'],
                                            outline=True,
                                            color="primary",
                                            className="w-15 mx-1",
                                            style={"border-radius": "50px"},
                                            href=link['link'],
                                            id=f"{id_prefix}-button-{index}"
                                        )
                                    )
                                    for index, link in enumerate(card_props.get('button_label', []))
                                ]
                            ),
                            html.P(
                                [
                                    html.P(
                                        dbc.CardLink(
                                            link["label"],
                                            href=link["link"],
                                            id=f"{id_prefix}-link-{index}"
                                        )
                                    )
                                    for index, link in enumerate(card_props.get("link_label", [{"label": "link 1", "link": "#"}]))
                                ]
                            )
                        ]
                    ),
                    dbc.CardImg(src=card_props.get("image_src", ""), bottom=True, id=f"{id_prefix}-image-bottom")
                    if card_props.get("image_position") != "top" else None,
                ],
                style={"width": "22.5rem"} if "style" not in card_props else card_props.get("style"),
                id=f"{id_prefix}-card"
            )
        )


class ContactPageCards(dbc.Card):
    def __init__(self, id_prefix=None, **card_props):
        if id_prefix is None:
            card_id = str(uuid.uuid4())
            id_prefix = f"contactpage-card-{card_id}"

        super(ContactPageCards, self).__init__(
            dbc.Card(
                dbc.CardBody(
                    [
                        dbc.CardImg(
                            src=card_props.get("image_src", ""),
                            className="image-container",
                            style={
                                'position': 'relative',
                                'width': '50px',
                                'height': '50px',
                                'overflow': 'hidden',
                                'marginBottom': '0'
                            },
                            id=f"{id_prefix}-image"
                        ),
                        html.H4(
                            card_props.get("card_title", "Card Title"),
                            className="card-title",
                            id=f"{id_prefix}-title"
                        ),
                        html.H6(
                            card_props.get("card_text", "Card Text"),
                            className="card-subtitle",
                            id=f"{id_prefix}-subtitle"
                        ),
                        dbc.Button(
                            "Register",
                            color="primary",
                            className="w-15 mx-1",
                            id=f"{id_prefix}-button"
                        )
                    ]
                ),
                id=f"{id_prefix}-card"
            )
        )


class ExploreCardOne(dbc.Card):
    def __init__(self, id_prefix=None, **card_props):
        if id_prefix is None:
            card_id = str(uuid.uuid4())
            id_prefix = f"explore-card-{card_id}"

        super(ExploreCardOne, self).__init__(
            dbc.Card(
                dbc.CardBody(
                    [
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        html.H4(
                                            card_props.get("card_title", "Card Title"),
                                            className="card-title",
                                            id=f"{id_prefix}-title"
                                        ),
                                        html.H6(
                                            card_props.get("card_text", "Card Text"),
                                            className="card-subtitle",
                                            id=f"{id_prefix}-text"
                                        ),
                                        html.P(
                                            [
                                                dbc.Button(
                                                    link['label'],
                                                    outline=True,
                                                    color="primary",
                                                    className="w-15 mx-1",
                                                    style={"border-radius": "50px"},
                                                    href=link['link'],
                                                    id=f"{id_prefix}-button-{i}"
                                                )
                                                for i, link in enumerate(card_props.get('button_label', []))
                                            ]
                                        )
                                    ]
                                ),
                                dbc.Col(
                                    dbc.Button(
                                        html.Span(">", className="align-middle"),
                                        outline=True,
                                        color="primary",
                                        className="vertical-button",
                                        style={"height": "200px", "width": "5px", "display": "flex",
                                               "justify-content": "center", "align-items": "center", "border": "none"},
                                        href="next_screen_link",
                                        id=f"{id_prefix}-next-button"
                                    ),
                                    width=3,
                                )
                            ],
                            className="align-items-start"
                        )
                    ]
                ),
                style={"width": "18rem"} if 'style' not in card_props else card_props.get('style'),
                id=f"{id_prefix}-card"
            )
        )


class FullWidthCard(dbc.Card):
    def __init__(self, id_prefix=None, **card_props):
        if id_prefix is None:
            card_id = str(uuid.uuid4())
            id_prefix = f"fullwidth-card-{card_id}"

        super(FullWidthCard, self).__init__(
            dbc.Card(
                [
                    dbc.Row([
                        dbc.Col(
                            dbc.CardImg(src=card_props.get("image_src", ""), id=f"{id_prefix}-image-left")
                        ) if card_props.get("image_position") == "left" else None,
                        dbc.Col(
                            dbc.CardBody([
                                dbc.CardImg(
                                    src=card_props.get("image_src", ""),
                                    className="image-container",
                                    style={
                                        'position': 'relative',
                                        'width': '50px',
                                        'height': '50px',
                                        'overflow': 'hidden',
                                        'marginBottom': '0'
                                    },
                                    id=f"{id_prefix}-image"
                                ),
                                html.H4(
                                    card_props.get("card_title", "Card Title"),
                                    className="card-title",
                                    id=f"{id_prefix}-title"
                                ),
                                html.H6(
                                    card_props.get("card_text", "Card Text"),
                                    className="card-subtitle",
                                    id=f"{id_prefix}-subtitle"
                                ),
                                html.Div(
                                    [
                                        html.P(
                                            dbc.Button(
                                                link['label'],
                                                outline=True,
                                                color="primary",
                                                className="w-15 mx-1",
                                                style={"border-radius": "50px"},
                                                href=link['link'],
                                                id=f"{id_prefix}-button-{index}"
                                            )
                                        )
                                        for index, link in enumerate(card_props.get('button_label', []))
                                    ]
                                )
                            ])
                        ),
                        dbc.Col(
                            dbc.CardImg(src=card_props.get("image_src", ""), id=f"{id_prefix}-image-right")
                        ) if card_props.get("image_position") != "left" else None,
                    ])
                ],
                style={"width": "18rem"} if 'style' not in card_props else card_props.get('style'),
                id=f"{id_prefix}-card"
            )
        )


class FullWidthCardtwo(dbc.Card):
    def __init__(self, id_prefix=None, **card_props):
        if id_prefix is None:
            card_id = str(uuid.uuid4())
            id_prefix = f"fullwidthtwo-card-{card_id}"

        super(FullWidthCardtwo, self).__init__(
            dbc.Card(
                [
                    dbc.CardImg(src=card_props.get("image_src", ""), top=True, id=f"{id_prefix}-image-top"),
                    dbc.CardBody([
                        dbc.CardImg(
                            src=card_props.get("image_src", ""),
                            className="image-container",
                            style={
                                'position': 'relative',
                                'width': '50px',
                                'height': '50px',
                                'overflow': 'hidden',
                                'marginBottom': '0'
                            },
                            id=f"{id_prefix}-image"
                        ),
                        html.H4(
                            card_props.get("card_title", "Card Title"),
                            className="card-title",
                            id=f"{id_prefix}-title"
                        ),
                        html.H6(
                            card_props.get("card_text", "Card Text"),
                            className="card-subtitle",
                            id=f"{id_prefix}-subtitle"
                        ),
                        html.Div(
                            [
                                html.P(
                                    dbc.Button(
                                        link['label'],
                                        outline=True,
                                        color="primary",
                                        className="w-15 mx-1",
                                        style={"border-radius": "50px"},
                                        href=link['link'],
                                        id=f"{id_prefix}-button-{index}"
                                    )
                                )
                                for index, link in enumerate(card_props.get('button_label', []))
                            ]
                        )
                    ]
                    )
                ],
                style={"width": "18rem"} if 'style' not in card_props else card_props.get('style'),
                id=f"{id_prefix}-card"
            )
        )


class HomePageCard(dbc.Card):
    def __init__(self, id_prefix=None, **card_props):
        if id_prefix is None:
            card_id = str(uuid.uuid4())
            id_prefix = f"homepage-card-{card_id}"

        super(HomePageCard, self).__init__(
            dbc.Card(
                dbc.CardBody(
                    [
                        html.Div(
                            dbc.CardImg(src=card_props.get("image_src", ""), id=f"{id_prefix}-image"),
                            className="image-container",
                            style={
                                'position': 'relative',
                                'width': '100px',
                                'height': '100px',
                                'overflow': 'hidden',
                                'marginBottom': '0'
                            }
                        ),
                        html.H4(
                            card_props.get("card_title", "Card Title"),
                            className="card-title",
                            id=f"{id_prefix}-title"
                        ),
                        html.H6(
                            card_props.get("card_text", "Card Text"),
                            className="card-subtitle",
                            id=f"{id_prefix}-subtitle"
                        ),
                        dbc.Button(
                            card_props.get("button_title"),
                            outline=True,
                            color="primary",
                            className="w-15 mx-1",
                            style={"border-radius": "50px"},
                            href='#',
                            id=f"{id_prefix}-button1"
                        ),
                        html.Hr(),
                        html.H6(
                            card_props.get("card_text2", "Card Text"),
                            className="card-subtitle",
                            id=f"{id_prefix}-subtitle2"
                        ),
                        dbc.Button(
                            card_props.get("button_title2"),
                            outline=True,
                            color="primary",
                            className="w-15 mx-1",
                            style={"border-radius": "50px"},
                            href='#',
                            id=f"{id_prefix}-button2"
                        ) if 'button_title2' not in card_props else None,
                    ]
                ),
                style={"width": "18rem"} if 'style' not in card_props else card_props.get('style'),
                id=f"{id_prefix}-card"
            )
        )


class OrderingCards(dbc.Card):
    def __init__(self, id_prefix=None, **card_props):
        image_style = {'backgroundImage': f"url({card_props.get('image_src', '')})",
                       'backgroundSize': 'cover',
                       'backgroundPosition': 'center',
                       'backgroundRepeat': 'no-repeat',
                       'padding': '20px'}

        if id_prefix is None:
            card_id = str(uuid.uuid4())
            id_prefix = f"ordering-card-{card_id}"

        super(OrderingCards, self).__init__(
            dbc.Card(
                dbc.CardBody(
                    [
                        html.H4(
                            card_props.get("card_title", "Card Title"),
                            className="card-title",
                            id=f"{id_prefix}-title"
                        ),
                        html.H6(
                            card_props.get("card_text", "Card Text"),
                            className="card-subtitle",
                            id=f"{id_prefix}-subtitle"
                        ),
                        html.Div(
                            [html.P(
                                dbc.Button(
                                    link['label'],
                                    outline=True,
                                    color="primary",
                                    className="w-15 mx-1",
                                    style={"border-radius": "50px"},
                                    href=link['link'],
                                    id=f"{id_prefix}-button-{index+1}"
                                )
                            ) for index, link in enumerate(card_props.get('button_label', []))]
                        )
                    ]
                ),
                style=image_style if 'style' not in card_props else {**image_style, **card_props.get('style')},
                id=f"{id_prefix}-card"
            )
        )


class QuickLinksCard(dbc.Card):
    def __init__(self, id_prefix=None, **card_props):
        if id_prefix is None:
            card_id = str(uuid.uuid4())
            id_prefix = f"quicklink-card-{card_id}"

        super(QuickLinksCard, self).__init__(
            dbc.Card(
                [
                    dbc.CardHeader(
                        card_props.get('card_title', "Card Title"),
                        style={"background-color": "#0000E7"},
                        id=f"{id_prefix}-header"
                    ),
                    dbc.CardBody(
                        [
                            html.Div(
                                [html.P(
                                    dbc.Button(
                                        link['label'],
                                        outline=True,
                                        color="primary",
                                        className="w-15 mx-1",
                                        style={"border-radius": "50px"},
                                        href=link['link'],
                                        id=f"{id_prefix}-button-{index+1}"
                                    )
                                ) for index, link in enumerate(card_props.get('button_label', []))]
                            ),
                            html.P(
                                [
                                    html.P(
                                        dbc.CardLink(
                                            link["label"],
                                            href=link["link"],
                                            id=f"{id_prefix}-link-{index+1}"
                                        )
                                    ) for index, link in enumerate(card_props.get("link_label", []))
                                ]
                            )
                        ]
                    )
                ],
                style={"width": "22.5rem"} if 'style' not in card_props else card_props.get('style'),
                id=f"{id_prefix}-card"
            )
        )


class SuggestTopicCard(dbc.Card):
    def __init__(self, id_prefix=None, **card_props):
        if id_prefix is None:
            card_id = str(uuid.uuid4())
            id_prefix = f"suggesttopic-card-{card_id}"

        super(SuggestTopicCard, self).__init__(
            dbc.Card(
                [
                    dbc.Row(
                        [
                            dbc.Col(
                                dbc.CardBody(
                                    [
                                        html.H4(
                                            card_props.get("card_title", "Card Title"),
                                            className="card-title",
                                            id=f"{id_prefix}-title"
                                        ),
                                        html.P(
                                            card_props.get("card_text", "Card Text"),
                                            className="card-text",
                                            id=f"{id_prefix}-text"
                                        ),
                                        dbc.Button(
                                            card_props.get("button_title", "Button Display"),
                                            outline=True,
                                            color="primary",
                                            className="w-100",
                                            style={"border-radius": "50px"},
                                            id=f"{id_prefix}-button"
                                        ),
                                    ]
                                ),
                                width=6,
                            ),
                            dbc.Col(
                                dbc.CardImg(
                                    src=card_props.get("image_src", ""),
                                    style={
                                        "max-width": "100%",
                                        "width": "570px",
                                        "height": "277px"
                                    },
                                    className="custom-image",
                                    id=f"{id_prefix}-image"
                                ),
                                width=6,
                            )
                        ],
                        className="g-0 d-flex align-items-center",
                        id=f"{id_prefix}-row"
                    )
                ],
                className="custom-card",
                style={
                    "width": "36rem",
                    "height": "12rem"
                } if 'style' not in card_props else card_props.get('style'),
                id=f"{id_prefix}-card"
            )
        )


class SuggestTopicCardTwo(dbc.Card):
    def __init__(self, id_prefix=None, **card_props):
        if id_prefix is None:
            card_id = str(uuid.uuid4())
            id_prefix = f"suggesttopictwo-card-{card_id}"

        super(SuggestTopicCardTwo, self).__init__(
            dbc.Card(
                [
                    dbc.CardImg(src=card_props.get("image_src", ""), top=True, id=f"{id_prefix}-image"),
                    dbc.CardBody(
                        [
                            html.H4(
                                card_props.get("card_title", "Card Title"),
                                className="card-title",
                                id=f"{id_prefix}-title"
                            ),
                            html.P(
                                card_props.get("card_text", "Card Text"),
                                className="card-text",
                                id=f"{id_prefix}-text"
                            ),
                            dbc.Button(
                                card_props.get("button_title", "Button Display"),
                                outline=True,
                                color="primary",
                                className="w-100",
                                style={"border-radius": "50px"},
                                id=f"{id_prefix}-button"
                            ),
                        ]
                    ),
                ],
                style={"width": "18rem"} if 'style' not in card_props else card_props.get('style'),
                id=f"{id_prefix}-card"
            )
        )