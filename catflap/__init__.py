import sass
import os

static_root = os.path.join(os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')), "catflapsite"),
                           "static")

sass.compile(dirname = (os.path.join(static_root, "sass"), os.path.join(static_root, "css")))
