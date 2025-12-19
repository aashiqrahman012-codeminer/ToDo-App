const API_BASE = 'http://127.0.0.1:8000';

document.getElementById('addBtn').onclick = async () => {
  const title = document.getElementById('taskInput').value.trim();
  if (!title) return;
  
  await fetch(`${API_BASE}/todos`, {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({title})
  });
  document.getElementById('taskInput').value = '';
  loadTasks();
  loadAnalytics();
};

const loadTasks = async () => {
  const res = await fetch(`${API_BASE}/todos`);
  const tasks = await res.json();
  const list = document.getElementById('tasksList');
  list.innerHTML = tasks.map(t => `
    <div class="task">
      <span class="${t.done ? 'done' : ''}">${t.title}</span>
      <button onclick="toggleDone(${t.id}, ${!t.done})">${t.done ? 'Undo' : 'Done'}</button>
      <button onclick="deleteTask(${t.id})">🗑️</button>
    </div>
  `).join('');
};

const toggleDone = async (id, done) => {
  await fetch(`${API_BASE}/todos/${id}`, {
    method: 'PUT',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({done})
  });
  loadTasks();
  loadAnalytics();
};

const deleteTask = async (id) => {
  if (!confirm('Delete?')) return;
  await fetch(`${API_BASE}/todos/${id}`, {method: 'DELETE'});
  loadTasks();
  loadAnalytics();
};

const loadAnalytics = async () => {
  const res = await fetch(`${API_BASE}/analytics`);
  const data = await res.json();
  const box = document.getElementById('analyticsBox');
  if (data.message) {
    box.innerHTML = `<p>${data.message}</p>`;
  } else {
    box.innerHTML = `
      <h3>📊 Analytics</h3>
      <p>Total: ${data.total_tasks} | Completed: ${data.completed_tasks}</p>
      <p>Rate: ${data.completion_rate_percent}% | This week: ${data.completed_this_week}</p>
    `;
  }
};

// Load on start
loadTasks();
loadAnalytics();