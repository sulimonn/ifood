
const password = document.getElementById('password');

function ButtonBegin(x) {
  let account = document.getElementsByClassName('roo')[0];
  console.log(account)
  if (account.style.display === 'none') {
    account.style.display = 'block';
  }
  window.addEventListener('click', (e) => {
    if (!e.target.className.includes('modalShow')) {
      account.style.display = 'none';
    }
  });
}

if(password !== undefined){
    let ch = '';
    for (let i in password.innerText.split('')) {
      ch += '*';
    }
    password.innerText = ch;
}


function subheader(){
    console.log(window.scrollY)
    if (window.pageYOffset >= 700){
        let subhead = document.getElementsByClassName('subhead')[0]
        subhead.className = 'subhead show'
    }
    else{
        let subhead = document.getElementsByClassName('subhead')[0]

        subhead.className = 'subhead hide'
    }
}
function registr(x){
  if(x){
      document.getElementById('reg').style.display = 'none'
      document.getElementById('auth').style.display = 'block'
  }
  else{
      document.getElementById('reg').style.display = 'block'
      document.getElementById('auth').style.display = 'none'
  }
}

window.addEventListener('scroll', ()=> subheader())
