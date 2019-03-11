class FormMixin(object):
    def get_errors(self):
        messages = []
        if hasattr(self, 'errors'):
            errors = self.errors.get_json_data()
            for message_dicts in errors.values():
                for message in message_dicts:
                    messages.append(message['message'])
            return messages[0]
        else:
            return {}

# 之前的提取错误消息的代码，得到的消息并不是很友好，重新修改了一下，没有使用ajax，所以看起来不是那么友好吧。
# class FormMixin(object):
#     def get_errors(self):
#         if hasattr(self, 'errors'):
#             errors = self.errors.get_json_data()
#             new_errors = {}
#             for key, message_dicts in errors.items():
#                 messages = []
#                 for message in message_dicts:
#                     messages.append(message['message'])
#                 new_errors[key] = messages
#             print(new_errors)
#             return new_errors
#         else:
#             return {}



