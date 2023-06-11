
    const elements = document.getElementsByClassName('reg__input')
    function translate(){
        for (const element of elements) {
            if (element.children[1].value !== '') {
                 element.children[0].className = 'full'
             } else {
                 element.children[0].className = 'empty'
            }
        }
    }
    for (const element of elements) {
        element.children[1].onchange = translate
    }
    translate()
