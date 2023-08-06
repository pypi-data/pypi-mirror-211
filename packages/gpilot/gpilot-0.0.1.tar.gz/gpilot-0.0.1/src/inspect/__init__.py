from pynput.mouse import Listener
import pika
import json

# publish all events from mouse to rabbitmq queue "mouse_events"
mq = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost')
)

ch = mq.channel()
ch.queue_declare(queue='mouse_events')

def on_move(x, y):
    """
    Print the pointer's x and y coordinates when it moves.

    :param x: an integer for the x coordinate of the pointer's new position
    :param y: an integer for the y coordinate of the pointer's new position
    :return: None
    """
    # publish events from listener to rabbitmq queue "mouse_events"
    ch.basic_publish(
        exchange='',
        routing_key='mouse_events',
        body=json.dumps({
            'x': x,
            'y': y,
            'type': 'move'
        }),
        properties=pika.BasicProperties(
            delivery_mode=2,
            content_type='application/json'
        )
    )


def on_click(x, y, button, pressed):
    """
    Listens for a mouse click event, prints whether the button was pressed or released,
    and stops the listener when the button is released.

    :param x: The x-coordinate of the mouse cursor at the time of the event.
    :type x: int
    :param y: The y-coordinate of the mouse cursor at the time of the event.
    :type y: int
    :param button: The button that was clicked.
    :type button: Button
    :param pressed: A boolean indicating whether the button was pressed (True) or released (False).
    :type pressed: bool
    :return: False if the button was released, indicating that the listener should stop.
    :rtype: bool
    """
    ch.basic_publish(
        exchange='',
        routing_key='mouse_events',
        body=json.dumps({
            'x': x,
            'y': y,
            'type': 'click'
        }),
        properties=pika.BasicProperties(
            delivery_mode=2,
            content_type='application/json'
        )
    )
    if not pressed:
        # Stop listener
        return False


def on_scroll(x, y, dx, dy):
    """
    This function is a callback function that is called when the user scrolls the mouse wheel.

    :param x: The x-coordinate of the mouse cursor.
    :param y: The y-coordinate of the mouse cursor.
    :param dx: The horizontal scroll distance.
    :param dy: The vertical scroll distance.
    :return: None
    """
    ch.basic_publish(
        exchange='',
        routing_key='mouse_events',
        body=json.dumps({
            'x': x,
            'y': y,
            'type': 'scroll'
        }),
        properties=pika.BasicProperties(
            delivery_mode=2,
            content_type='application/json'
        )
    )


def main():
    """
    Runs the main event listener, which collects events until released.

    :param None
    :return: None
    """
    with Listener(
            on_move=on_move,
            on_click=on_click,
            on_scroll=on_scroll) as listener:
        
        while listener.running:
            listener.join()
            
        listener.stop()

if __name__ == '__main__':
    main()
