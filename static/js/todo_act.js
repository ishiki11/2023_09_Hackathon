/* ==================================================
			要素の取得
    ================================================== */
//audio要素を取得
let audio = document.getElementById('audio');
//表示箇所の要素取得
let durationDisplay = document.getElementById('durationDisplay');
let currentTimeDisplay = document.getElementById('currentTimeDisplay');
let volumeDisplay = document.getElementById('volumeDisplay');
//操作ボタンの取得
let volumeRange = document.getElementById('volumeRange');

/* ==================================================
			音声の操作と情報の取得
    ================================================== */
//音声ファイルの読み込み完了時の操作
//（音声ファイル読み込み前に情報を取得しようとしても正常に取得できないので注意）
audio.addEventListener('loadedmetadata', function () {
  /* --------------------------------------------------
				音声の情報取得
			-------------------------------------------------- */
  //音声全体の時間を取得(秒数がミリ秒単位で取得される)
  durationDisplay.textContent = timeConvert(audio.duration);

  //現在の再生時間の取得
  audio.addEventListener('timeupdate', function () {
    currentTimeDisplay.textContent = timeConvert(audio.currentTime);
  });

  //ステータスの取得
  audio.addEventListener('timeupdate', function () {
    console.log('再生位置の変化');
  });
  audio.addEventListener('ended', function () {
    console.log('再生完了');
  });

  /* --------------------------------------------------
				音声の操作
			-------------------------------------------------- */

  //音量調節レンジ初期設定（inputの初期値と表示の値）
  volumeRange.value = audio.volume;
  volumeDisplay.textContent = (audio.volume * 100).toFixed(0);

  //音量調節レンジの動作
  volumeRange.addEventListener('input', function () {
    //rangeの値をaudio.volumeに設定する
    audio.volume = volumeRange.value;
    //rangeの値を表示
    volumeDisplay.textContent = (volumeRange.value * 100).toFixed(0);
  });
});

/* ==================================================
			必要な関数の設定
    ================================================== */
//時間をmm:ss表記にする関数
function timeConvert(time) {
  var floorTime = Math.floor(time);
  var min = Math.floor(floorTime / 60).toFixed(0);
  var sec = ('00' + (floorTime % 60).toFixed(0)).slice(-2);
  return min + ':' + sec;
}
