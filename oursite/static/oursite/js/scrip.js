
document.body.addEventListener('scroll', () => {
    let subhead = document.getElementsByClassName('subhead')[0]
    if (window.scrollY >= 700){
        subhead.className = 'subhead show'
    }
    else{
        subhead.className = 'subhead hide'
    }
})


function ButtonBegin(x) {
  let account = document.getElementsByClassName('roo')[0];
  if (account.style.display === 'none') {
    account.style.display = 'block';
  }
  window.addEventListener('click', (e) => {
    if (!e.target.className.includes('modalShow')) {
      account.style.display = 'none';
    }
  });
}
