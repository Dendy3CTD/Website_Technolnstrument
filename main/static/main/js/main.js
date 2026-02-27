/**
 * Каталог промышленных инструментов — фильтры, сортировка, корзина (оптимизировано)
 */
(function () {
  'use strict';

  var productGrid = document.getElementById('productGrid');
  var resultsCount = document.getElementById('resultsCount');
  var resultsCountSpan = resultsCount && resultsCount.querySelector('span');
  var sortSelect = document.getElementById('sort');
  var filterReset = document.getElementById('filterReset');
  var loadMoreBtn = document.getElementById('loadMore');
  var cartCountEl = document.querySelector('.header-icon__count, .cart-btn__count');
  var btnMenu = document.getElementById('btnMenu');
  var slidePanel = document.getElementById('slidePanel');
  var panelOverlay = document.getElementById('panelOverlay');
  var panelClose = document.getElementById('panelClose');
  var btnFilters = document.getElementById('btnFilters');
  var filterOverlay = document.getElementById('filterOverlay');
  var filterPanel = document.getElementById('filterPanel');
  var filterPanelClose = document.getElementById('filterPanelClose');
  var btnAccount = document.getElementById('btnAccount');
  var authOverlay = document.getElementById('authOverlay');
  var authModal = document.getElementById('authModal');
  var authModalClose = document.getElementById('authModalClose');
  var authSwitchTab = document.getElementById('authSwitchTab');
  var authTabPhone = document.getElementById('authTabPhone');
  var authTabEmail = document.getElementById('authTabEmail');
  var authFormPhone = document.getElementById('authFormPhone');
  var authFormEmail = document.getElementById('authFormEmail');
  var authModalTitle = document.getElementById('authModalTitle');

  var cartCount = 0;

  function setBodyOverflow(locked) {
    document.body.style.overflow = locked ? 'hidden' : '';
  }

  function setBodyOverflowNextFrame(locked) {
    requestAnimationFrame(function () { setBodyOverflow(locked); });
  }

  function needLockBody() {
    return (slidePanel && slidePanel.classList.contains('is-open')) ||
           (filterPanel && filterPanel.classList.contains('is-open')) ||
           (authModal && authModal.classList.contains('is-open'));
  }

  function unlockBodyAfterClose() {
    if (!needLockBody()) setBodyOverflowNextFrame(false);
  }

  // --- Один обработчик Escape для всех панелей ---
  document.addEventListener('keydown', function (e) {
    if (e.key !== 'Escape') return;
    if (authModal && authModal.classList.contains('is-open')) {
      authModal.classList.remove('is-open');
      if (authOverlay) authOverlay.classList.remove('is-open');
      if (btnAccount) btnAccount.setAttribute('aria-expanded', 'false');
      unlockBodyAfterClose();
      return;
    }
    if (filterPanel && filterPanel.classList.contains('is-open')) {
      filterPanel.classList.remove('is-open');
      if (filterOverlay) filterOverlay.classList.remove('is-open');
      if (btnFilters) btnFilters.setAttribute('aria-expanded', 'false');
      unlockBodyAfterClose();
      return;
    }
    if (slidePanel && slidePanel.classList.contains('is-open')) {
      slidePanel.classList.remove('is-open');
      if (panelOverlay) panelOverlay.classList.remove('is-open');
      if (btnMenu) btnMenu.setAttribute('aria-expanded', 'false');
      unlockBodyAfterClose();
    }
  }, { passive: true });

  // --- Личный кабинет (auth) ---
  function openAuthModal() {
    if (authModal) authModal.classList.add('is-open');
    if (authOverlay) authOverlay.classList.add('is-open');
    if (btnAccount) btnAccount.setAttribute('aria-expanded', 'true');
    setBodyOverflowNextFrame(true);
  }
  function closeAuthModal() {
    if (authModal) authModal.classList.remove('is-open');
    if (authOverlay) authOverlay.classList.remove('is-open');
    if (btnAccount) btnAccount.setAttribute('aria-expanded', 'false');
    unlockBodyAfterClose();
  }
  if (btnAccount) btnAccount.addEventListener('click', openAuthModal);
  if (authModalClose) authModalClose.addEventListener('click', closeAuthModal);
  if (authOverlay) authOverlay.addEventListener('click', closeAuthModal);

  function showAuthTab(tab) {
    var isEmail = tab === 'email';
    if (authTabPhone) authTabPhone.classList.toggle('is-active', !isEmail);
    if (authTabEmail) authTabEmail.classList.toggle('is-active', isEmail);
    if (authModalTitle) authModalTitle.textContent = isEmail ? 'Введите e-mail' : 'Введите номер телефона';
    if (authSwitchTab) authSwitchTab.textContent = isEmail ? 'Войти по номеру телефона' : 'Войти по e-mail';
  }
  if (authSwitchTab) authSwitchTab.addEventListener('click', function () {
    showAuthTab(authTabEmail && authTabEmail.classList.contains('is-active') ? 'phone' : 'email');
  });

  if (authFormPhone) authFormPhone.addEventListener('submit', function (e) {
    e.preventDefault();
    var phone = document.getElementById('authPhone');
    if (phone && !phone.value.trim()) return;
    closeAuthModal();
  });
  if (authFormEmail) authFormEmail.addEventListener('submit', function (e) {
    e.preventDefault();
    var email = document.getElementById('authEmail');
    if (email && !email.value.trim()) return;
    closeAuthModal();
  });

  // --- Панель фильтров ---
  function openFilterPanel() {
    if (filterPanel) filterPanel.classList.add('is-open');
    if (filterOverlay) filterOverlay.classList.add('is-open');
    if (btnFilters) btnFilters.setAttribute('aria-expanded', 'true');
    setBodyOverflowNextFrame(true);
  }
  function closeFilterPanel() {
    if (filterPanel) filterPanel.classList.remove('is-open');
    if (filterOverlay) filterOverlay.classList.remove('is-open');
    if (btnFilters) btnFilters.setAttribute('aria-expanded', 'false');
    unlockBodyAfterClose();
  }
  if (btnFilters) btnFilters.addEventListener('click', openFilterPanel);
  if (filterPanelClose) filterPanelClose.addEventListener('click', closeFilterPanel);
  if (filterOverlay) filterOverlay.addEventListener('click', closeFilterPanel);

  // --- Слайд-меню ---
  function openPanel() {
    if (slidePanel) slidePanel.classList.add('is-open');
    if (panelOverlay) panelOverlay.classList.add('is-open');
    if (btnMenu) btnMenu.setAttribute('aria-expanded', 'true');
    setBodyOverflowNextFrame(true);
  }
  function closePanel() {
    if (slidePanel) slidePanel.classList.remove('is-open');
    if (panelOverlay) panelOverlay.classList.remove('is-open');
    if (btnMenu) btnMenu.setAttribute('aria-expanded', 'false');
    unlockBodyAfterClose();
  }
  if (btnMenu) btnMenu.addEventListener('click', openPanel);
  if (panelClose) panelClose.addEventListener('click', closePanel);
  if (panelOverlay) panelOverlay.addEventListener('click', closePanel);

  // --- Сворачивание блоков фильтров: делегирование ---
  var filterPanelBody = filterPanel && filterPanel.querySelector('.filter-panel__body');
  if (filterPanelBody) {
    filterPanelBody.addEventListener('click', function (e) {
      var btn = e.target.closest('[data-filter-toggle]');
      if (!btn) return;
      var expanded = btn.getAttribute('aria-expanded') !== 'false';
      btn.setAttribute('aria-expanded', expanded ? 'false' : 'true');
    });
  }

  // --- Сброс фильтров ---
  function updateResultsCount(n) {
    if (resultsCountSpan) resultsCountSpan.textContent = n;
  }

  if (filterReset) {
    filterReset.addEventListener('click', function () {
      var container = filterPanel || document;
      var checkboxes = container.querySelectorAll('.filters input[type="checkbox"]');
      for (var i = 0; i < checkboxes.length; i++) checkboxes[i].checked = false;
      var inputs = container.querySelectorAll('.filter-range__input');
      for (var j = 0; j < inputs.length; j++) inputs[j].value = '';
      if (sortSelect) sortSelect.value = 'popular';
      updateResultsCount(productGrid ? productGrid.children.length : 0);
    });
  }

  // --- Сортировка: один reflow через DocumentFragment ---
  function parsePrice(el) {
    if (!el) return 0;
    return parseInt(el.textContent.replace(/\s|\u20BD/g, ''), 10) || 0;
  }

  if (sortSelect && productGrid) {
    sortSelect.addEventListener('change', function () {
      var value = this.value;
      var items = Array.prototype.slice.call(productGrid.querySelectorAll('.product-card'));
      if (value === 'price-asc' || value === 'price-desc') {
        items.sort(function (a, b) {
          var priceA = parsePrice(a.querySelector('.product-card__price-current'));
          var priceB = parsePrice(b.querySelector('.product-card__price-current'));
          return value === 'price-asc' ? priceA - priceB : priceB - priceA;
        });
        var frag = document.createDocumentFragment();
        for (var i = 0; i < items.length; i++) frag.appendChild(items[i]);
        productGrid.appendChild(frag);
      }
      updateResultsCount(items.length);
    });
  }

  // --- Кнопка «В корзину»: делегирование на сетке (включая динамически добавленные карточки) ---
  if (productGrid) {
    productGrid.addEventListener('click', function (e) {
      var btn = e.target.closest('.product-card__cart');
      if (!btn || btn.disabled) return;
      e.preventDefault();
      cartCount += 1;
      if (cartCountEl) cartCountEl.textContent = cartCount;
      btn.textContent = 'В корзине';
      btn.disabled = true;
    });
  }

  // --- Показать ещё: один append через DocumentFragment, без новых слушателей ---
  if (loadMoreBtn && productGrid) {
    loadMoreBtn.addEventListener('click', function () {
      var first = productGrid.querySelector('.product-card');
      if (!first) return;
      var frag = document.createDocumentFragment();
      for (var i = 0; i < 6; i++) {
        var clone = first.cloneNode(true);
        var cartBtn = clone.querySelector('.product-card__cart');
        if (cartBtn) {
          cartBtn.textContent = 'В корзину';
          cartBtn.disabled = false;
        }
        frag.appendChild(clone);
      }
      productGrid.appendChild(frag);
      updateResultsCount(productGrid.querySelectorAll('.product-card').length);
    });
  }
})();
