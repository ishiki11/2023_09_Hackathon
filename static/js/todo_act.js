//audio要素を取得
let audio = document.getElementById('audio');
// src取得
let source = audio.querySelector('source');
let src = source.getAttribute('src');
//音声操作
let playMusic = document.getElementById('play-music');
let volumeRange = document.getElementById('volumeRange');
// mute切り替え
let muteImg = document.getElementById('img');
// タイマー操作
let totalTime = document.getElementById('total-time');
let BreakTime = document.getElementById('for-breaktime');
let breakText = document.getElementById('break-text');
// 作業中か休憩中かのサークル
let workCircle = document.getElementById('work-circle');
let breakCircle = document.getElementById('break-circle');

isMute = false; //ミュート状態か

//音声ファイルの読み込み完了時の操作
//（音声ファイル読み込み前に情報を取得しようとしても正常に取得できないので注意）
audio.addEventListener('loadedmetadata', function () {
  //音量調節レンジ初期設定（inputの初期値と表示の値）
  audio.volume = 0;
  volumeRange.value = audio.volume;
  //音量調節レンジの動作
  volumeRange.addEventListener('input', function () {
    if (!isMute) {
      //rangeの値をaudio.volumeに設定する
      audio.volume = volumeRange.value;
    }
  });
});

// フェードイン
let fadeInInterval;
function fadeIn() {
  const targetVolume = 0.5; // フェードインで変化する音量
  const fadeDuration = 10000; // フェードにかかる時間（ミリ秒）
  const interval = 100; // フェードの更新間隔（ミリ秒）
  const step = (targetVolume - audio.volume) / (fadeDuration / interval);
  let cnt = fadeDuration / interval;
  fadeInInterval = setInterval(() => {
    audio.volume += step;
    volumeRange.value = audio.volume;
    cnt--;
    if (cnt == 0 || audio.volume >= 1) {
      clearInterval(fadeInInterval);
    }
  }, interval);
}

// フェードアウト
let fadeOutInterval;
function fadeOut() {
  const targetVolume = 0; // フェードアウト後の目標音量
  const fadeDuration = 10000; // フェードにかかる時間（ミリ秒）
  const interval = 100; // フェードの更新間隔（ミリ秒）
  const step = (targetVolume - audio.volume) / (fadeDuration / interval);
  let cnt = fadeDuration / interval;
  fadeOutInterval = setInterval(() => {
    audio.volume += step;
    volumeRange.value = audio.volume;
    cnt--;
    if (cnt === 0 || audio.volume <= 0) {
      clearInterval(fadeOutInterval);
    }
  }, interval);
}

/**
 * ミュート状態の切り替え
 */
function switchMute() {
  isMute = !isMute;
  if (isMute) {
    audio.volume = 0;
    clearInterval(fadeInInterval);
    clearInterval(fadeOutInterval);
    muteImg.src = '/static/images/mute.png';
  } else {
    audio.volume = volumeRange.value;
    muteImg.src = '/static/images/volume.png';
  }
}

let isBreak = false; //休憩中か
/**
 * 音楽切り替え関数
 */
function switchMusic() {
  if (!isBreak) {
    var MusicSrc = todoData[6]; //作業音楽に切り替え
    playMusic.textContent = todoData[5];
  } else {
    var MusicSrc = todoData[4]; //休憩音楽に切り替え
    playMusic.textContent = todoData[3];
  }
  // srcを変える
  audio.querySelector('source').setAttribute('src', MusicSrc);
  if (!isMute) {
    // <audio>要素を再読み込みして新しい音楽を再生
    audio.load();
    fadeIn();
  }
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
  fadeIn();
  startTotalTimer(); // トータル時間の計測
  breakTimer(); // 休憩までの時間
}

// タイマーstart
let totalSeconds = 0;
function startTotalTimer() {
  timerInterval = setInterval(() => {
    totalSeconds++;
    totalTime.textContent = formatTime(totalSeconds);
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
    if (forSeconds === 10) {
      if (!isMute) {
        fadeOut();
      }
    }
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
  forSeconds = 20; // 発表用
  breakText.textContent = '休憩までの時間：';
  BreakTime.textContent = formatTime(forSeconds);
}

// 残りの休憩時間：
function setRestBreak() {
  // 残りの休憩時間
  forSeconds = 5 * 60;
  forSeconds = 20; // 発表用
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

// 完了ボタンの押された時
function finishBtn() {
  stopTime();
  audio.pause();

  seconds = totalSeconds;
  todo_id = todoData[0];
  const data = { seconds, todo_id };

  fetch('/todo_act', {
    method: 'POST',
    headers: { 'Content-type': 'application/json; charset=utf-8' },
    body: JSON.stringify(data),
  })
    .then((response) => {
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      return response.json();
    })
    .then((data) => {
      console.log(data.message);
      // jsonデータのチェック
      if (data.flag) {
        window.location.replace('/todo_list');
      } else {
        window.location.replace('/');
      }
    })
    .catch((error) => {
      console.error('Error', error);
    });
}
