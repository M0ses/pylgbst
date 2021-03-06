import logging
import time
import traceback

from examples.plotter import Plotter
from pylgbst.comms import DebugServerConnection, BLEConnection


def moves():
    plotter.move(-FIELD_WIDTH, 0)
    plotter.move(FIELD_WIDTH * 2, 0)
    plotter.move(-FIELD_WIDTH, 0)

    plotter.move(FIELD_WIDTH, FIELD_WIDTH)
    plotter.move(-FIELD_WIDTH, -FIELD_WIDTH)

    plotter.move(0, FIELD_WIDTH)
    plotter.move(0, -FIELD_WIDTH)


def cross():
    plotter.line(FIELD_WIDTH, FIELD_WIDTH)
    plotter.move(-FIELD_WIDTH, 0)
    plotter.line(FIELD_WIDTH, -FIELD_WIDTH)


def square():
    plotter.line(FIELD_WIDTH, 0)
    plotter.line(0, FIELD_WIDTH)
    plotter.line(-FIELD_WIDTH, 0)
    plotter.line(0, -FIELD_WIDTH)


def triangle():
    plotter.line(FIELD_WIDTH, 0)
    plotter.line(0, FIELD_WIDTH)
    plotter.line(-FIELD_WIDTH, -FIELD_WIDTH)


def romb():
    plotter.move(-FIELD_WIDTH, 0)
    plotter.line(FIELD_WIDTH, FIELD_WIDTH * 2)
    plotter.line(FIELD_WIDTH, -FIELD_WIDTH * 2)
    plotter.line(-FIELD_WIDTH, -FIELD_WIDTH * 2)
    plotter.line(-FIELD_WIDTH, FIELD_WIDTH * 2)


def circles():
    plotter.move(FIELD_WIDTH / 4.0, 0)
    plotter.circle(FIELD_WIDTH / 2.0)

    plotter.move(FIELD_WIDTH / 2.0, 0)
    plotter.circle(FIELD_WIDTH)


class LaserPlotter(Plotter):

    def _tool_down(self):
        super(LaserPlotter, self)._tool_down()
        time.sleep(1)


def lego():
    t = FIELD_WIDTH / 5.0
    h = t * 5.0
    w = t * 3.0

    plotter.move(-t * 2.0, 0)

    plotter.line(h, 0)
    plotter.line(0, t)
    plotter.line(-(h - t), 0)
    plotter.line(0, 2 * t)
    plotter.line(-t, 0)
    plotter.line(0, -w)

    plotter.move(0, w + t)

    plotter.line(h, 0)
    plotter.line(0, w)
    plotter.line(-t, 0)
    plotter.line(0, -2 * t)
    plotter.line(-t, 0)
    plotter.line(0, t)
    plotter.line(-t, 0)
    plotter.line(0, -t)
    plotter.line(-t, 0)
    plotter.line(0, 2 * t)
    plotter.line(-t, 0)
    plotter.line(0, -w)

    plotter.move(0, w + t)

    plotter.move(t, 0)
    plotter.line(3 * t, 0)
    plotter.line(t, t)
    plotter.line(0, t)
    plotter.line(-t, t)
    plotter.line(-t, 0)
    plotter.line(0, -t)
    plotter.line(t, 0)
    plotter.line(0, -t)
    plotter.line(-3 * t, 0)
    plotter.line(0, t)
    plotter.line(t, 0)
    plotter.line(0, t)
    plotter.line(-3 * t, 0)
    plotter.line(0, -t)
    plotter.line(t, 0)
    plotter.line(0, -t)
    plotter.line(t, -t)
    plotter.move(-t, 0)

    plotter.move(0, w + t)

    plotter.move(t, 0)
    plotter.line(3 * t, 0)
    plotter.line(t, t)
    plotter.line(0, t)
    plotter.line(-t, t)
    plotter.line(-3 * t, 0)
    plotter.line(-t, -t)
    plotter.line(0, -t)
    plotter.line(t, -t)
    plotter.move(0, t)
    plotter.line(3 * t, 0)
    plotter.line(0, t)
    plotter.line(-3 * t, 0)
    plotter.line(0, -t)


def square_spiral():
    rounds = 7
    step = FIELD_WIDTH / 4.0 / rounds
    for r in range(1, rounds):
        plotter.line(step * r * 4, 0)
        plotter.line(0, step * (r * 4 + 1))
        plotter.line(-step * (r * 4 + 2), 0)
        plotter.line(0, -step * (r * 4 + 3))


def christmas_tree():
    t = FIELD_WIDTH / 5
    plotter.line(t, t)
    plotter.line(-t * 0.5, 0)
    plotter.line(t, t)
    plotter.line(-t * 0.5, 0)
    plotter.line(t, t)

    plotter.line(-t * 3.5, 0)

    plotter.line(t, -t)
    plotter.line(-t * 0.5, 0)
    plotter.line(t, -t)
    plotter.line(-t * 0.5, 0)
    plotter.line(t, -t)


def try_speeds():
    speeds = [x * 1.0 / 10.0 for x in range(1, 11)]
    for s in speeds:
        logging.info("%s", s)
        plotter.motor_AB.constant(s, -s)
        time.sleep(1)
    for s in reversed(speeds):
        logging.info("%s", s)
        plotter.motor_AB.constant(-s, s)
        time.sleep(1)


def snowflake():
    a = [300, 232,
         351, 144,
         307, 68,
         350, 45,
         379, 94,
         413, 36,
         456, 61,
         422, 119,
         482, 118,
         481, 167,
         394, 168,
         343, 256,
         444, 256,
         488, 179,
         530, 204,
         500, 256,
         569, 256,
         582, 280]
    prev = None
    vals = []
    maxval = 0
    for i in range(0, len(a)):
        if i % 2:
            continue

        maxval = max(maxval, abs(a[i]), abs(a[i + 1]))
        if prev:
            vals.append((a[i] - prev[0], a[i + 1] - prev[1]))
        prev = a[i], a[i + 1]

    assert len(vals) == len(a) / 2 - 1

    vals = [(x[0] / float(maxval), x[1] / float(maxval)) for x in vals]

    logging.info("Moves: %s", vals)
    zoom = FIELD_WIDTH * 2.0
    for item in vals:
        plotter.line(item[0] * zoom, item[1] * zoom)

    for item in reversed(vals):
        plotter.line(-item[0] * zoom, item[1] * zoom)

    for item in vals:
        plotter.line(-item[0] * zoom, -item[1] * zoom)

    for item in reversed(vals):
        plotter.line(item[0] * zoom, -item[1] * zoom)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    try:
        conn = DebugServerConnection()
    except BaseException:
        logging.warning("Failed to use debug server: %s", traceback.format_exc())
        conn = BLEConnection().connect()

    plotter = LaserPlotter(conn, 0.75)
    FIELD_WIDTH = plotter.field_width

    try:
        plotter.initialize()

        # plotter._tool_down()

        # try_speeds()

        # moves()
        # triangle()
        # square()
        # cross()
        # romb()
        # circles()
        # plotter.spiral(4, 0.02)
        # plotter.rectangle(FIELD_WIDTH / 5.0, FIELD_WIDTH / 5.0, solid=True)

        # square_spiral()
        # lego()
        # christmas_tree()
        snowflake()
        pass
    finally:
        plotter.finalize()
