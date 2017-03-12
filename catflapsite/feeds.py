from django.contrib.syndication.views import Feed
import catflapsite.utils as kitty

class CatFood(Feed):
    title = "Cat Flap RSS"
    link = "/catfood/"
    description = "A list of pictures, generally alternating between my cat's face and bum," \
                  "as he exits and returns through the cat flap. Occasionally featuring human feet," \
                  "hands, and other body parts (usually still attached to the rest of the body)."

    def items(self):
        return [k for k in kitty.get_key_objects() if k.iscat]

    def item_title(self, item):
        return str(item.time_taken)

    def item_description(self, item):
        return "is this a cat? if not, mark it as such by clicking the little cat icon on the history page!"

    def item_link(self, item):
        return "/history/"

    def item_enclosure_url(self, item):
        return item.url.split("?")[0]

    def item_enclosure_length(self, item):
        return item.size

    def item_enclosure_mime_type(self, item):
        return "image/jpeg"
