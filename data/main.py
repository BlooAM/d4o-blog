from faker import Faker
from faker_blog import BlogProvider

fake = Faker()
fake.add_provider(BlogProvider)


if __name__ == '__main__':
    for _ in range(10):
        title = fake.article_title_and_slug()
        print(f'TITLE_W_SLUG: {title}')
        content_html = fake.article_content_html()
        print(f'CONTENT HTML: {content_html}')
        image = fake.article_image()
        print(f'IMAGE: {image}\n')
