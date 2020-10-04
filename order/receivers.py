from django.db.models.signals import post_save
from django.dispatch import receiver

from catalog.models import MailBox
from order.models import Order, OrderItem
from order.signals import order_payed


@receiver(post_save, sender=OrderItem, dispatch_uid='order_item_counter_buy_increase')
def post_save_order_item_counter_buy_increase(sender, instance, **kwargs):
    # This is an experiment with signals.
    # It's not necessary to increase buy counter here
    order_item_id = instance
    order_item = OrderItem.objects.select_related('orderitem').get(order_item_id=str(order_item_id))
    item = order_item.orderitem
    item.update_counter_buy()


@receiver(order_payed, sender=Order)
def receive_order_payed(sender, order, user, **kwargs):
    # This is an experiment with signals.
    # It's not necessary to form and create an email to managers group here to inform them about order was paid
    MailBox.objects.create(order_id=order.order_id,
                           subject='Заказ {0} оплачен клиентом {1}'.format(order, user),
                           body='Необходимо подтвердить заказ у клиента: почта={0}, id={1}'.format(
                               user, user.id),
                           customer=user)
