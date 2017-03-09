from django.contrib.syndication.views import Feed
import catflapsite.utils as kitty


class CatFood(Feed):
    title = "Cat Flap RSS"
    link = "/catfood/"
    description = "A list of pictures, generally alternating between my cat's face and bum," \
                  "as he exits and returns through the cat flap. Occasionally featuring human feet," \
                  "hands, and other body parts (usually still attached to the rest of the body)."

    def items(self):
        return [k for k in kitty.get_key_objects() if k.iscat()]

    def item_title(self, item):
        return str(item.time_taken)

    def item_description(self, item):
        if item.iscat(kitty.load_tags()):
            return "hi/bye cat"
        else:
            return "that's no cat"

    def item_link(self, item):
        return item.url
