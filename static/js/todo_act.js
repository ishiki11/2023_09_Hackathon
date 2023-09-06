//audio要素を取得
let audio = document.getElementById('audio');
// src取得
let source = audio.querySelector('source');
let src = source.getAttribute('src');
//音声操作
let playMusic = document.getElementById('play-music');
let volumeRange = document.getElementById('volumeRange');
// タイマー操作
let totalTime = document.getElementById('total-time');
let BreakTime = document.getElementById('for-breaktime');
let breakText = document.getElementById('break-text');
// 作業中か休憩中かのサークル
let workCircle = document.getElementById('work-circle');
let breakCircle = document.getElementById('break-circle');

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

let isBreak = false; //休憩中か
/**
 * 音楽切り替え関数
 */
function switchMusic() {
  if (!isBreak) {
    var MusicSrc = todoData[5]; //作業音楽に切り替え
    playMusic.textContent = todoData[4];
  } else {
    var MusicSrc = todoData[3]; //休憩音楽に切り替え
    playMusic.textContent = todoData[2];
  }
  // srcを変える
  audio.querySelector('source').setAttribute('src', MusicSrc);
  // <audio>要素を再読み込みして新しい音楽を再生
  audio.load();
}

/**
 * 実行中かのランプ切り替え
 */
function switchCircle() {
  if (!isBreak) {
    workCircle.style.backgroundColor = 'green';
    breakCircle.style.backgroundColor = 'white';
  } else {
    workCircle.style.backgroundColor = 'white';
    breakCircle.style.backgroundColor = 'red';
  }
}

/**
 * タイマー機能
 */
function timerStart() {
  startTotalTimer(); // トータル時間の計測
  breakTimer(); // 休憩までの時間
}

// タイマーstart
function startTotalTimer() {
  let seconds = 0;
  timerInterval = setInterval(() => {
    seconds++;
    totalTime.textContent = formatTime(seconds);
  }, 1000); // 1秒ごとにカウントアップ
}

// タイマーstop
function stopTime() {
  clearInterval(timerInterval);
  clearInterval(breakInterval);
}

let forSeconds = 0; //休憩までの時間
// 25分と5分の計測
function breakTimer() {
  setForBreak(); //休憩までの時間
  breakInterval = setInterval(() => {
    forSeconds--;
    BreakTime.textContent = formatTime(forSeconds);
    if (forSeconds === 0) {
      if (isBreak) {
        //休憩の時
        setForBreak(); //文字と時間の設定
        isBreak = !isBreak;
        switchMusic();
        switchCircle();
      } else {
        // 作業中の時
        setRestBreak();
        isBreak = !isBreak;
        switchMusic();
        switchCircle();
      }
    }
  }, 1000);
}

// 休憩時間までの設定
function setForBreak() {
  //休憩までの時間
  forSeconds = 25 * 60;
  // forSeconds = 10; // 発表用
  breakText.textContent = '休憩までの時間：';
  BreakTime.textContent = formatTime(forSeconds);
}

// 残りの休憩時間：
function setRestBreak() {
  // 残りの休憩時間
  forSeconds = 5 * 60;
  // forSeconds = 5; // 発表用
  breakText.textContent = '残りの休憩時間：';
  BreakTime.textContent = formatTime(forSeconds);
}

// 画面読み込みでタイマースタートする
window.addEventListener('load', timerStart);

// 時間をh時間mm分ss秒表記にする関数
function formatTime(seconds) {
  const hours = Math.floor(seconds / 3600);
  const formattedHours = String(hours).padStart(1, '0');
  const minutes = Math.floor((seconds % 3600) / 60);
  const formattedMinutes = String(minutes).padStart(2, '0');
  const remainingSeconds = seconds % 60;
  const formattedSeconds = String(remainingSeconds).padStart(2, '0');
  if (seconds >= 3600) {
    return `${formattedHours}時間${formattedMinutes}分${formattedSeconds}秒`;
  } else if (seconds >= 60) {
    return `${formattedMinutes}分${formattedSeconds}秒`;
  } else {
    return `${formattedSeconds}秒`;
  }
}

// 完了ボタンの削除
function finishBtn() {
  stopTime();
  audio.pause();
}
