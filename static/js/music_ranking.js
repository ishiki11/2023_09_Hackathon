// タブ
let workTab = document.getElementById('work-tab');
let breakTab = document.getElementById('break-tab');
// ボタン
let workBtn = document.getElementById('work-btn')
let breakBtn = document.getElementById('break-btn')


function showTab(tab) {
  console.log(tab);
  if (tab == "work") {
    workBtn.style.backgroundColor = '#E1E1E1';
    breakBtn.style.backgroundColor = 'white';
    breakTab.style.display = 'none';
    workTab.style.display = '';
  }
  if (tab == "break") {
    breakBtn.style.backgroundColor = '#E1E1E1';
    workBtn.style.backgroundColor = 'white';
    workTab.style.display = 'none';
    breakTab.style.display = '';
  }
}