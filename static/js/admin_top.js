document.addEventListener("DOMContentLoaded", function () {
  var searchInput = document.getElementById("search");

  searchInput.addEventListener("input", function () {
    var query = searchInput.value;

    fetch("/admin/top", {
      method: "POST",
      headers: {
        "Content-Type": "application/json; charset=utf-8"
      },
      body: JSON.stringify(query)
    })
    .then((response) => {
      return response.json();
    })
    .then((data) => {
      // テーブルのtbody要素を取得
      const tbody = document.querySelector(".user-list tbody");
      tbody.innerHTML = ""; // テーブルの内容をクリア
      data.data.forEach((user) => {
        const row = document.createElement("tr");
        row.innerHTML = `
          <td class="user">${user[1]}</td>
          <td class="mail">${user[3]}</td>
          <td class="point">${user[2]}</td>
          <td class="delete">
              <a href="{{ url_for('admin_top.user_delete', param=${user[0]}) }}" class="delete-a">削除</a>
          </td>
        `;
        tbody.appendChild(row);
      });
    })
    .catch((error) => {
        console.error("エラーが発生しました:", error);
    });
  });
});