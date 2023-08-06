from behave import step


@step("Open '{url}'")
@step('Open "{url}"')
def open_url(context, url):
    sb = context.sb
    sb.open(url)


@step("Click element '{selector}'")
@step('Click element "{selector}"')
def click_element(context, selector):
    sb = context.sb
    sb.click(selector)


@step("Type text '{text}' into '{selector}'")
@step('Type text "{text}" into "{selector}"')
def type_text_into_element(context, text, selector):
    sb = context.sb
    sb.assert_text(text, selector)


@step("Into '{selector}' type '{text}' ")
@step('Into "{selector}" type "{text}" ')
def into_element_type_text(context, selector, text):
    sb = context.sb
    sb.assert_text(text, selector)


@step("Assert element '{selector}'")
@step('Assert element "{selector}"')
def assert_element(context, selector):
    sb = context.sb
    sb.assert_element(selector)


@step("Assert text '{text}' in '{selector}'")
@step('Assert text "{text}" in "{selector}"')
def assert_text_in_element(context, text, selector):
    sb = context.sb
    sb.assert_text(text, selector)


@step("Assert text '{text}'")
@step('Assert text "{text}"')
def assert_text(context, text):
    sb = context.sb
    sb.assert_text(text)


@step("Assert exact text '{text}' in '{selector}'")
@step('Assert exact text "{text}" in "{selector}"')
def assert_exact_text(context, text, selector):
    sb = context.sb
    sb.assert_exact_text(text, selector)


@step("Highlight '{selector}'")
@step('Highlight "{selector}"')
def highlight_element(context, selector):
    sb = context.sb
    sb.highlight(selector)


@step("Click link '{link}'")
@step('Click link "{link}"')
def click_link(context, link):
    sb = context.sb
    sb.click_link(link)


@step("Save screenshot to logs")
def save_screenshot_to_logs(context):
    sb = context.sb
    sb.save_screenshot_to_logs()


@step("Clear Local Storage")
def clear_local_storage(context):
    sb = context.sb
    sb.clear_local_storage()


@step("Clear Session Storage")
def clear_session_storage(context):
    sb = context.sb
    sb.clear_session_storage()
