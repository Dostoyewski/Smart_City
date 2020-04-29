/**
 * Turns html text into a normal one.
 */
function render(messageHTML) {
    let element = document.createElement('div')
    element.innerHTML = messageHTML
    return element.textContent
}