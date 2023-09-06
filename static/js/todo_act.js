//audio要素を取得
let audio = document.getElementById('audio');
// src取得
let source = audio.querySelector('source');
let src = source.getAttribute('src');
console.log(src);
//音声操作
let volumeRange = document.getElementById('volumeRange');

//音声ファイルの読み込み完了時の操作
//（音声ファイル読み込み前に情報を取得しようとしても正常に取得できないので注意）
audio.addEventListener('loadedmetadata', function () {
  //音量調節レンジ初期設定（inputの初期値と表示の値）
  volumeRange.value = audio.volume;
  //音量調節レンジの動作
  volumeRange.addEventListener('input', function () {
    //rangeの値をaudio.volumeに設定する
    audio.volume = volumeRange.value;
  });
});

// 休憩音楽に切り替える
function switchbreakMusic() {
  var breakMusicSrc = '{{ data[3] }}';
}

// 作業用音楽に切り替え

//時間をmm:ss表記にする関数
function timeConvert(time) {
  var floorTime = Math.floor(time);
  var min = Math.floor(floorTime / 60).toFixed(0);
  var sec = ('00' + (floorTime % 60).toFixed(0)).slice(-2);
  return min + ':' + sec;
}
