class Article_obj:

    def __init__(self, a_title, a_slug, a_content, a_tag, a_source, a_date, a_images):
        self.title=a_title
        self.slug=a_slug
        self.content=a_content
        self.tag=a_tag
        self.source=a_source
        self.date=a_date
        self.images=a_images

    def __repr__(self):
        return "Article ({}, {}, {}, {}, {})".format(self.title, self.tag, self.date, self.slug, self.images)