from django.utils import timezone

from django.shortcuts import get_object_or_404
from django.core.mail import send_mail

from config.settings import EMAIL_HOST_USER
from mailings.models import Mailing, MailingAttempt


# from datetime import timezone
# from typing import Any
#
# from catalog.models import Product
# from config.settings import CACHE_ENABLED
# from django.core.cache import cache
#
#
# class ProductService:
#
#     @staticmethod
#     def get_products_by_category(category_id: int) -> Any:
#         """ Возвращает QuerySet (продукты) по идентификатору категории """
#         products = Product.objects.filter(category_id=category_id)
#         if not products.exists():
#             return None
#         return products
#
#     @staticmethod
#     def get_products_by_category_cached(category_id: int) -> Any:
#         """ Проверяет подключение кеширования и в положительном случае возвращает QuerySet из кеша """
#         if not CACHE_ENABLED:
#             return ProductService.get_products_by_category(category_id)
#         queryset = cache.get('products_by_category')
#         if not queryset:
#                 queryset = ProductService.get_products_by_category(category_id)
#                 cache.set('products_by_category', queryset, 10)
#         return queryset
#
#
# def attempt_details():
#     date_and_time = timezone.now()

class MailingService:

    @staticmethod
    def send_mailing(pk):
        mailing = get_object_or_404(Mailing, pk=pk)
        if mailing.status != 'Завершена':
            try:
                send_mail(
                    subject=mailing.message.subject,
                    message=mailing.message.body,
                    from_email=EMAIL_HOST_USER,
                    recipient_list=mailing.get_related_fields().split(', '),
                    fail_silently=False)
                mailing.status = 'Запущена'
                mailing.first_sending = timezone.now()
            except Exception as e:
                server_reply_for_attempt = e
            finally:
                mailing.save()
                if mailing.status == 'Запущена':
                    attempt_status = MailingAttempt.SUCCESSFUL
                    server_reply = ''
                else:
                    attempt_status = MailingAttempt.UNSUCCESSFUL
                    server_reply = server_reply_for_attempt

            return MailingAttempt.objects.create(date_time_of_attempt=timezone.now(), status=attempt_status,
                                                 server_reply=server_reply,
                                                 mailing=mailing)
