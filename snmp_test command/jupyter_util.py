from IPython.display import display, HTML

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

    def warp(*args, **kwargs):
        if not __is_notebook():
            raise RuntimeError(f"This function: {func.__name__} should be used in jupyter environment.\n")
            return
        else:
            func(*args, **kwargs)
    return warp


def __get_copyboard_templete_HTML(text="text\nto\ncopy"):

    templete_head = f"""
    <label for="show2copy">Show to copy:</label><br>
    <textarea id="show2copy" name="show2copy" style="font-size: 1pt" rows="5" cols="33"
    >{text}\n</textarea><br>
    """
    #
    templete_fucntion = """
    <button onclick="myFunction()">Copy text</button>
    
    
    <script type="text/javascript">
        function myFunction() {
              var copyText = document.getElementById("show2copy");
    
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
    pass
    putting_clipboard("fw")