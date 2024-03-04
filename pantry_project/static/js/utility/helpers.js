/**
 *  initializes the buttons (usually sort/filter buttons)
 *
 * @param {Array.<HTMLElement>} btns - array of buttons to initialize
 * @param {Array.<string>} selected - array to store the selected values
 * @param {string} cssActiveClass - the class to add to the button when it is active
 * @param {boolean} multiSelect - if true, multiple buttons can be active at once
 */
export function initButtons(
  btns,
  selected,
  cssActiveClass,
  multiSelect = false
) {
  btns.forEach((btn) => {
    btn.onclick = () => {
      let value = btn.value;

      // user is deselecting
      if (selected.includes(value)) {
        btn.classList.remove(cssActiveClass);
        selected.splice(selected.indexOf(value), 1);
        return false;
      }

      // user is selecting another value
      if (!multiSelect) {
        btns.forEach((btn) => {
          btn.classList.remove(cssActiveClass);
        });
        selected.length = 0;
      }
      btn.classList.add(cssActiveClass);
      selected.push(value);
      return false;
    };
  });
}