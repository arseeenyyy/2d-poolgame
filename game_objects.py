import pymunk
from settings import dia

balls = []
rows = 5

def create_ball(radius, pos, space):
    body = pymunk.Body()
    body.position = pos
    shape = pymunk.Circle(body, radius)
    shape.mass = 5
    shape.elasticity = 0.8
    pivot = pymunk.PivotJoint(space.static_body, body, (0, 0), (0, 0))
    pivot.max_bias = 0
    pivot.max_force = 1000

    space.add(body, shape, pivot)
    return shape

#pockets on the table
pockets = [
    (55, 63),
    (592, 48),
    (1134, 64),
    (55, 616),
    (592, 629),
    (1134, 616)
]

#create cushions
cushions = [
    [(88, 56), (109, 77), (555, 77), (564, 56)],
    [(621, 56), (630, 77), (1081, 77), (1102, 56)],
    [(89, 621), (110, 600), (556, 600), (564, 621)],
    [(622, 621), (630, 600), (1081, 600), (1102, 621)],
    [(56, 96), (77, 117), (77, 560), (56, 581)],
    [(1143, 96), (1122, 117), (1122, 560), (1143, 581)]
]

def create_cushion(poly_dims, space):
    body = pymunk.Body(body_type=pymunk.Body.STATIC)
    body.position = (0, 0)
    shape = pymunk.Poly(body, poly_dims)
    shape.elasticity = 0.8
    space.add(body, shape)

def initialize_balls(space):
    global balls
    rows = 5
    for col in range(5):
        for row in range(rows):
            pos = (250 + (col * (dia + 1)), 267 + (row * (dia + 1)) + (col * dia / 2))
            new_ball = create_ball(dia / 2, pos, space)
            balls.append(new_ball)
        rows -= 1

    cue_ball = create_ball(dia / 2, (888, 678 / 2), space)
    balls.append(cue_ball)
    return cue_ball

initial_positions = [
    (250 + (col * (dia + 1)), 267 + (row * (dia + 1)) + (col * dia / 2))
    for col in range(5) for row in range(5 - col)
]
cue_ball_position = (888, 678 / 2)
cue_ball = None  
__all__ = ["create_ball", "create_cushion", "pockets", "balls", "cue_ball", "cushions", "initialize_balls"]