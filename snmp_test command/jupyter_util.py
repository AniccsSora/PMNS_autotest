from IPython.display import display, HTML
import random

CHAR_SET = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
NUMB_SET = "0123456789"


def get_random_id(digit=10):
    head = 2
    h = "".join([random.choice(CHAR_SET) for _ in range(head)])
    b = "".join([random.choice(CHAR_SET+NUMB_SET) for _ in range(digit-head)])
    return h+b


def __is_notebook() -> bool:
    """
    check running environment.
    :return:
    """
    try:
        shell = get_ipython().__class__.__name__
        if shell == 'ZMQInteractiveShell':
            return True   # Jupyter notebook or qtconsole
        elif shell == 'TerminalInteractiveShell':
            return False  # Terminal running IPython
        else:
            return False  # Other type (?)
    except NameError:
        return False      # Probably standard Python interpreter


def should_run_on_jupyter(func):
    def do_nothing(*args, **kwargs):
        pass

    def warp(*args, **kwargs):
        if not __is_notebook():
            # raise RuntimeError(f"This function: {func.__name__} should be used in jupyter environment.\n")
            return do_nothing(*args, **kwargs)
        else:
            func(*args, **kwargs)
    return warp


def __get_copyboard_templete_HTML(text="text\nto\ncopy"):
    RAND_ID = get_random_id()
    #print(f"TEXT = \"{text}\"")
    import time
    time.sleep(0.3)
    templete_head = f"""
    <label for="{RAND_ID}">Show to copy:</label><br>
    <textarea id="{RAND_ID}" name="{RAND_ID}" style="font-size: 1pt" rows="5" cols="139"
    >{text}\n</textarea><br>
    """
    #
    templete_fucntion = f"""
    <button onclick="myFunction_{RAND_ID}()">Copy text</button>
    <script type="text/javascript">"""+\
    f"""function myFunction_{RAND_ID}()"""+\
        """ 
        {
              var copyText = 
              """ + f'document.getElementById("{RAND_ID}");' + \
    """
              copyText.select();
              copyText.setSelectionRange(0, 99999);
              navigator.clipboard.writeText(copyText.value);
              //alert("Copied the text: " + copyText.value);
        }
    </script>
    """
    return HTML(templete_head+templete_fucntion)


@should_run_on_jupyter
def putting_clipboard(want2copy_text=None):
    if want2copy_text is None:
        html = __get_copyboard_templete_HTML()
    else:
        html = __get_copyboard_templete_HTML(want2copy_text)
    display(html)


if __name__ == "__main__":
    for i in range(10):
        print(get_random_id())
