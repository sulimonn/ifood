
const elements = document.getElementsByClassName('translate')

let i;
console.log(elements.item('0'))
for (i = 0; i < elements.length; i++) {
    console.log(i)
  if (elements[i] instanceof HTMLElement) {
      console.log(elements[i])
  }

}

