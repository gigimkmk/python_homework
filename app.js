const API_URL = 'https://jsonplaceholder.typicode.com/todos';

const state = {
  todos: [],
  currentPage: 1,
  perPage: 10,
  filters: {
    search: '',
    userId: 'all',
    completed: 'all',
  },
};

const page = document.body.dataset.page;

async function fetchTodos() {
  try {
    const response = await fetch(API_URL);
    if (!response.ok) {
      throw new Error(`Request failed with status ${response.status}`);
    }

    const data = await response.json();
    state.todos = data;
    populateUserFilter();

    if (page === 'index') {
      renderDashboard();
    } else if (page === 'details') {
      renderDetails();
    }
  } catch (error) {
    showError(error.message);
  }
}

function populateUserFilter() {
  const select = document.getElementById('userFilter');
  if (!select) return;

  const uniqueUserIds = [...new Set(state.todos.map((todo) => todo.userId))].sort((a, b) => a - b);
  select.innerHTML = '<option value="all">All users</option>';

  uniqueUserIds.forEach((userId) => {
    const option = document.createElement('option');
    option.value = String(userId);
    option.textContent = `User ${userId}`;
    select.appendChild(option);
  });

  select.value = state.filters.userId;
}

function getFilteredTodos() {
  const searchValue = state.filters.search.trim().toLowerCase();

  return state.todos.filter((todo) => {
    const matchesSearch = !searchValue || todo.title.toLowerCase().includes(searchValue);
    const matchesUser = state.filters.userId === 'all' || String(todo.userId) === state.filters.userId;
    const matchesCompleted =
      state.filters.completed === 'all' ||
      (state.filters.completed === 'completed' && todo.completed) ||
      (state.filters.completed === 'incomplete' && !todo.completed);

    return matchesSearch && matchesUser && matchesCompleted;
  });
}

function renderDashboard() {
  const searchInput = document.getElementById('searchInput');
  const userFilter = document.getElementById('userFilter');
  const statusFilter = document.getElementById('statusFilter');
  const summary = document.getElementById('summary');
  const listContainer = document.getElementById('todoList');
  const pagination = document.getElementById('pagination');

  if (!searchInput || !userFilter || !statusFilter || !summary || !listContainer || !pagination) {
    return;
  }

  searchInput.value = state.filters.search;
  userFilter.value = state.filters.userId;
  statusFilter.value = state.filters.completed;

  const filteredTodos = getFilteredTodos();
  const totalPages = Math.max(1, Math.ceil(filteredTodos.length / state.perPage));

  if (state.currentPage > totalPages) {
    state.currentPage = totalPages;
  }

  summary.textContent = `Showing ${filteredTodos.length} todo(s) across ${state.todos.length} total records`;

  const startIndex = (state.currentPage - 1) * state.perPage;
  const pageItems = filteredTodos.slice(startIndex, startIndex + state.perPage);

  if (!pageItems.length) {
    listContainer.innerHTML = '<div class="empty-state">No todos match your search and filter settings.</div>';
    pagination.innerHTML = '';
    return;
  }

  listContainer.innerHTML = pageItems
    .map(
      (todo) => `
        <a class="todo-card" href="./details.html?id=${todo.id}">
          <div class="todo-card-header">
            <span class="todo-id">#${todo.id}</span>
            <span class="status-tag ${todo.completed ? 'completed' : 'pending'}">
              ${todo.completed ? 'Completed' : 'Pending'}
            </span>
          </div>
          <h2>${escapeHtml(todo.title)}</h2>
        </a>
      `
    )
    .join('');

  const prevButton = document.createElement('button');
  prevButton.className = 'page-btn';
  prevButton.textContent = 'Previous';
  prevButton.disabled = state.currentPage === 1;
  prevButton.addEventListener('click', () => {
    if (state.currentPage > 1) {
      state.currentPage -= 1;
      renderDashboard();
    }
  });

  const pageButtons = [];
  for (let pageNumber = 1; pageNumber <= totalPages; pageNumber += 1) {
    const btn = document.createElement('button');
    btn.className = `page-btn ${pageNumber === state.currentPage ? 'active' : ''}`;
    btn.textContent = String(pageNumber);
    btn.disabled = pageNumber === state.currentPage;
    btn.addEventListener('click', () => {
      state.currentPage = pageNumber;
      renderDashboard();
    });
    pageButtons.push(btn);
  }

  const nextButton = document.createElement('button');
  nextButton.className = 'page-btn';
  nextButton.textContent = 'Next';
  nextButton.disabled = state.currentPage === totalPages;
  nextButton.addEventListener('click', () => {
    if (state.currentPage < totalPages) {
      state.currentPage += 1;
      renderDashboard();
    }
  });

  pagination.innerHTML = '';
  pagination.append(prevButton, ...pageButtons, nextButton);
}

function renderDetails() {
  const container = document.getElementById('todoDetails');
  if (!container) return;

  const todoId = Number(new URLSearchParams(window.location.search).get('id'));
  const todo = state.todos.find((item) => item.id === todoId);

  if (!todo) {
    container.innerHTML = '<div class="empty-state">Todo not found.</div>';
    return;
  }

  container.innerHTML = `
    <div class="detail-grid">
      <div class="detail-item">
        <span class="detail-label">ID</span>
        <div class="detail-value">#${todo.id}</div>
      </div>
      <div class="detail-item">
        <span class="detail-label">User ID</span>
        <div class="detail-value">${todo.userId}</div>
      </div>
      <div class="detail-item">
        <span class="detail-label">Status</span>
        <div class="detail-value">${todo.completed ? 'Completed' : 'Pending'}</div>
      </div>
      <div class="detail-item">
        <span class="detail-label">Completed</span>
        <div class="detail-value">${todo.completed ? 'Yes' : 'No'}</div>
      </div>
      <div class="detail-item" style="grid-column: 1 / -1;">
        <span class="detail-label">Title</span>
        <div class="detail-value">${escapeHtml(todo.title)}</div>
      </div>
    </div>
  `;
}

function showError(message) {
  const listContainer = document.getElementById('todoList');
  const detailsContainer = document.getElementById('todoDetails');

  if (listContainer) {
    listContainer.innerHTML = `<div class="empty-state">Unable to load todos: ${escapeHtml(message)}</div>`;
  }

  if (detailsContainer) {
    detailsContainer.innerHTML = `<div class="empty-state">Unable to load todo details: ${escapeHtml(message)}</div>`;
  }
}

function escapeHtml(value) {
  return String(value)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#039;');
}

function attachIndexHandlers() {
  const searchInput = document.getElementById('searchInput');
  const userFilter = document.getElementById('userFilter');
  const statusFilter = document.getElementById('statusFilter');
  const resetButton = document.getElementById('resetFilters');

  if (!searchInput || !userFilter || !statusFilter || !resetButton) {
    return;
  }

  searchInput.addEventListener('input', (event) => {
    state.filters.search = event.target.value;
    state.currentPage = 1;
    renderDashboard();
  });

  userFilter.addEventListener('change', (event) => {
    state.filters.userId = event.target.value;
    state.currentPage = 1;
    renderDashboard();
  });

  statusFilter.addEventListener('change', (event) => {
    state.filters.completed = event.target.value;
    state.currentPage = 1;
    renderDashboard();
  });

  resetButton.addEventListener('click', () => {
    state.filters.search = '';
    state.filters.userId = 'all';
    state.filters.completed = 'all';
    state.currentPage = 1;
    renderDashboard();
  });
}

if (page === 'index') {
  attachIndexHandlers();
}

fetchTodos();
