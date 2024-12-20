document.getElementById('allergyForm').addEventListener('submit', async function(event) {
  event.preventDefault(); // ページリロードを防止

  const formData = {
    name: document.getElementById('name').value,
    allergy: document.getElementById('allergy').value,
    severity: document.getElementById('severity').value,
    treatment: document.getElementById('treatment').value,
  };

  try {
    // バックエンドにデータを送信
    base_url = 'https://allergy-service-hswx.onrender.com'
    //base_url = 'http://127.0.0.1:8000'
    const response = await fetch(`${base_url}/register`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(formData),
    });

    const result = await response.json();
    if (response.ok) {
      document.getElementById('responseMessage').textContent = result.message;
      // TODO innerHTMLは安全性に問題あり
      document.getElementById('shareLink').innerHTML = `<a href="${result.link}" target="_blank">共有リンク: ${result.link}</a>`;
    } else {
      document.getElementById('responseMessage').textContent = result.message;
    }
  } catch (error) {
    console.error('エラーが発生しました:', error);
    document.getElementById('responseMessage').textContent = "エラーが発生しました。再試行してください。";
  }
});
