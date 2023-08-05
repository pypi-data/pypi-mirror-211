/**
 * SimpleAdaptiveSlider by itchief v2.0.1 (https://github.com/itchief/ui-components/tree/master/simple-adaptive-slider)
 * Copyright 2020 - 2022 Alexander Maltsev
 * Licensed under MIT (https://github.com/itchief/ui-components/blob/master/LICENSE)
 */

class ItcSimpleSlider {
  // Базовые классы и селекторы.
  static PREFIX = 'slider';
  static CLASS_NAME_ITEM = `${ItcSimpleSlider.PREFIX}__item`;
  static CLASS_NAME_ITEM_ACTIVE = `${ItcSimpleSlider.PREFIX}__item_active`;
  static CLASS_NAME_ITEMS = `${ItcSimpleSlider.PREFIX}__items`;
  static CLASS_NAME_INDICATOR = `${ItcSimpleSlider.PREFIX}__indicator`;
  static CLASS_NAME_INDICATOR_ACTIVE = `${ItcSimpleSlider.PREFIX}__indicator_active`;
  static CLASS_NAME_INDICATORS = `${ItcSimpleSlider.PREFIX}__indicators`;
  static CLASS_NAME_CONTROL = `${ItcSimpleSlider.PREFIX}__control`;
  static CLASS_NAME_CONTROL_PREV = `${ItcSimpleSlider.PREFIX}__control_prev`;
  static CLASS_NAME_CONTROL_NEXT = `${ItcSimpleSlider.PREFIX}__control_next`;
  static CLASS_NAME_CONTROL_SHOW = `${ItcSimpleSlider.PREFIX}__control_show`;
  static SELECTOR_ITEMS = `.${ItcSimpleSlider.CLASS_NAME_ITEMS}`;
  static SELECTOR_ITEM = `.${ItcSimpleSlider.CLASS_NAME_ITEM}`;
  static SELECTOR_ITEM_ACTIVE = `.${ItcSimpleSlider.CLASS_NAME_ITEM_ACTIVE}`;
  static SELECTOR_INDICATOR_ACTIVE = `.${ItcSimpleSlider.CLASS_NAME_INDICATOR_ACTIVE}`;
  static SELECTOR_INDICATORS = `.${ItcSimpleSlider.CLASS_NAME_INDICATORS}`;
  static SELECTOR_WRAPPER = `.${ItcSimpleSlider.PREFIX}__wrapper`;
  static SELECTOR_CONTROL = `.${ItcSimpleSlider.CLASS_NAME_CONTROL}`;
  static SELECTOR_CONTROL_NEXT = `.${ItcSimpleSlider.CLASS_NAME_CONTROL_NEXT}`;
  static SELECTOR_CONTROL_PREV = `.${ItcSimpleSlider.CLASS_NAME_CONTROL_PREV}`;
  // порог для переключения слайда (20%)
  static SWIPE_THRESHOLD = 20;
  // класс для отключения transition
  static TRANSITION_NONE = 'transition-none';

  // Поддерживает ли текущий клиент пассивные события.
  static checkSupportPassiveEvents() {
    let passiveSupported = false;
    try {
      const options = Object.defineProperty({}, 'passive', {
        get() {
          passiveSupported = true;
        },
      });
      window.addEventListener('testPassiveListener', null, options);
      window.removeEventListener('testPassiveListener', null, options);
    } catch (error) {
      passiveSupported = false;
    }
    return passiveSupported;
  }

  constructor(target, config) {
    this._el = typeof target === 'string' ? document.querySelector(target) : target;
    this._elWrapper = this._el.querySelector(ItcSimpleSlider.SELECTOR_WRAPPER);
    this._elItems = this._el.querySelector(ItcSimpleSlider.SELECTOR_ITEMS);
    this._elsItem = this._el.querySelectorAll(ItcSimpleSlider.SELECTOR_ITEM);

    // текущий индекс
    this._currentIndex = 0;

    // экстремальные значения слайдов
    this._minOrder = 0;
    this._maxOrder = 0;
    this._$itemWithMinOrder = null;
    this._$itemWithMaxOrder = null;
    this._minTranslate = 0;
    this._maxTranslate = 0;

    // направление смены слайдов (по умолчанию)
    this._direction = 'next';

    // текущее значение трансформации
    this._transform = 0;

    this._width = this._elWrapper.getBoundingClientRect().width;

    this._supportResizeObserver = typeof window.ResizeObserver !== 'undefined';

    // swipe параметры
    this._hasSwipeState = false;
    this._swipeStartPosX = 0;

    // конфигурация слайдера (по умолчанию)
    const defaultConfig = {
      indicators: true,
      swipe: true,
    };
    this._config = Object.assign(defaultConfig, config);
    this._elItems.dataset.translate = 0;

    // добавляем к слайдам data-атрибуты
    this._elsItem.forEach((item, index) => {
      item.dataset.order = index;
      item.dataset.index = index;
      item.dataset.translate = 0;
    });

    // добавляем индикаторы к слайдеру
    this._addIndicators();
    // обновляем экстремальные значения переменных
    this._refreshExtremeValues();
    // помечаем активные элементы
    this._setActiveClass();
    // назначаем обработчики
    this._addEventListener();
  }

  // установка нужных классов
  _setActiveClass() {
    const elActive = this._el.querySelector(ItcSimpleSlider.SELECTOR_ITEM_ACTIVE);
    elActive ? elActive.classList.remove(ItcSimpleSlider.CLASS_NAME_ITEM_ACTIVE) : null;
    const elActiveNew = this._el.querySelector(`[data-index="${this._currentIndex}"]`);
    elActiveNew ? elActiveNew.classList.add(ItcSimpleSlider.CLASS_NAME_ITEM_ACTIVE) : null;

    const elIndicatorActive = this._el.querySelector(ItcSimpleSlider.SELECTOR_INDICATOR_ACTIVE);
    elIndicatorActive ? elIndicatorActive.classList.remove(ItcSimpleSlider.CLASS_NAME_INDICATOR_ACTIVE) : null;
    const elIndicatorNew = this._el.querySelector(`[data-slide-to="${this._currentIndex}"]`);
    elIndicatorNew ? elIndicatorNew.classList.add(ItcSimpleSlider.CLASS_NAME_INDICATOR_ACTIVE) : null;

    const elPrevBtn = this._el.querySelector(ItcSimpleSlider.SELECTOR_CONTROL_PREV);
    const elNextBtn = this._el.querySelector(ItcSimpleSlider.SELECTOR_CONTROL_NEXT);
    elPrevBtn ? elPrevBtn.classList.add(ItcSimpleSlider.CLASS_NAME_CONTROL_SHOW) : null;
    elNextBtn ? elNextBtn.classList.add(ItcSimpleSlider.CLASS_NAME_CONTROL_SHOW) : null;
    if (this._currentIndex === 0) {
      elPrevBtn.classList.remove(ItcSimpleSlider.CLASS_NAME_CONTROL_SHOW);
    } else if (this._currentIndex === this._elsItem.length - 1) {
      elNextBtn.classList.remove(ItcSimpleSlider.CLASS_NAME_CONTROL_SHOW);
    }
  }

  // смена слайдов
  _move(useTransition) {
    let translateX;
    this._elItems.classList.remove(ItcSimpleSlider.TRANSITION_NONE);

    if (useTransition === false) {
      this._elItems.classList.add(ItcSimpleSlider.TRANSITION_NONE);
    }

    if (this._direction === 'none') {
      translateX = this._transform * this._width;
      this._elItems.style.transform = `translateX(${translateX}px)`;
      return;
    }

    if (this._currentIndex + 1 >= this._elsItem.length && this._direction === 'next') {
      return;
    }
    if (this._currentIndex <= 0 && this._direction === 'prev') {
      return;
    }

    const step = this._direction === 'next' ? -1 : 1;
    const transform = this._transform + step;
    if (this._direction === 'next') {
      if (++this._currentIndex > this._elsItem.length - 1) {
        this._currentIndex -= this._elsItem.length;
      }
    } else if (--this._currentIndex < 0) {
      this._currentIndex += this._elsItem.length;
    }

    this._transform = transform;
    this._elItems.dataset.translate = transform;
    translateX = transform * this._width;
    this._elItems.style.transform = `translateX(${translateX}px)`;
    this._setActiveClass();
  }

  // функция для перемещения к слайду по индексу
  _moveTo(index, useTransition) {
    const currentIndex = this._currentIndex;
    this._direction = index > currentIndex ? 'next' : 'prev';

    for (let i = 0; i < Math.abs(index - currentIndex); i++) {
      this._move(useTransition);
    }
  }

  // добавление индикаторов
  _addIndicators() {
    if (this._el.querySelector(ItcSimpleSlider.SELECTOR_INDICATORS) || !this._config.indicators) {
      return;
    }
    let html = '';
    for (let i = 0, length = this._elsItem.length; i < length; i++) {
      html += `<li class="${ItcSimpleSlider.CLASS_NAME_INDICATOR}" data-slide-to="${i}"></li>`;
    }
    this._el.insertAdjacentHTML('beforeend', `<ol class="${ItcSimpleSlider.CLASS_NAME_INDICATORS}">${html}</ol>`);
  }

  // обновление значений переменных
  _refreshExtremeValues() {
    this._minOrder = parseInt(this._elsItem[0].dataset.order, 10);
    this._maxOrder = this._minOrder;
    this._$itemWithMinOrder = this._elsItem[0];
    this._$itemWithMaxOrder = this._$itemWithMinOrder;
    this._minTranslate = parseInt(this._elsItem[0].dataset.translate, 10);
    this._maxTranslate = this._minTranslate;
    for (let i = 0, length = this._elsItem.length; i < length; i++) {
      const $item = this._elsItem[i];
      const order = parseInt($item.dataset.order, 10);
      if (order < this._minOrder) {
        this._minOrder = order;
        this._$itemWithMinOrder = $item;
        this._minTranslate = parseInt($item.dataset.translate, 10);
      } else if (order > this._maxOrder) {
        this._maxOrder = order;
        this._$itemWithMaxOrder = $item;
        this._maxTranslate = parseInt($item.dataset.translate, 10);
      }
    }
  }

  // привязка к событиям
  _addEventListener() {
    function onClick(e) {
      const $target = e.target;
      if ($target.classList.contains(ItcSimpleSlider.CLASS_NAME_CONTROL)) {
        e.preventDefault();
        this._direction = $target.dataset.slide;
        this._move();
      } else if ($target.dataset.slideTo) {
        e.preventDefault();
        const index = parseInt($target.dataset.slideTo, 10);
        this._moveTo(index);
      }
    }

    function onSwipeStart(e) {
      if (e.target.closest(`.${ItcSimpleSlider.CLASS_NAME_CONTROL}`) || e.which != 1) {
        return;
      }

      const event = e.type.search('touch') === 0 ? e.touches[0] : e;
      this._swipeStartPosX = event.clientX;
      this._swipeStartPosY = event.clientY;
      this._hasSwipeState = true;
      this._hasSwiping = false;
    }

    function onSwipeMove(e) {
      if (!this._hasSwipeState) {
        return;
      }
      const event = e.type.search('touch') === 0 ? e.touches[0] : e;
      let diffPosX = this._swipeStartPosX - event.clientX;
      const diffPosY = this._swipeStartPosY - event.clientY;
      if (!this._hasSwiping) {
        if (Math.abs(diffPosY) > Math.abs(diffPosX) || Math.abs(diffPosX) === 0) {
          this._hasSwipeState = false;
          return;
        }
        this._hasSwiping = true;
      }
      e.preventDefault();
      const isBeforeFirst = this._currentIndex + 1 >= this._elsItem.length && diffPosX >= 0;
      const isAfterLast = this._currentIndex <= 0 && diffPosX <= 0;
      if (isBeforeFirst || isAfterLast) {
        diffPosX /= 4;
      }
      this._width = this._elWrapper.getBoundingClientRect().width;
      this._elItems.classList.add(ItcSimpleSlider.TRANSITION_NONE);
      const translateX = this._transform * this._width - diffPosX;
      this._elItems.style.transform = `translateX(${translateX}px)`;
    }

    function onSwipeEnd(e) {
      if (!this._hasSwipeState) {
        return;
      }
      const event = e.type.search('touch') === 0 ? e.changedTouches[0] : e;
      let diffPosX = this._swipeStartPosX - event.clientX;
      if (diffPosX === 0) {
        this._hasSwipeState = false;
        return;
      }

      const isBeforeFirst = this._currentIndex + 1 >= this._elsItem.length && diffPosX >= 0;
      const isAfterLast = this._currentIndex <= 0 && diffPosX <= 0;
      if (isBeforeFirst || isAfterLast) {
        diffPosX = 0;
      }

      const value = (diffPosX / this._elWrapper.getBoundingClientRect().width) * 100;
      this._elItems.classList.remove(ItcSimpleSlider.TRANSITION_NONE);
      if (value > ItcSimpleSlider.SWIPE_THRESHOLD) {
        this._direction = 'next';
        this._move();
      } else if (value < -ItcSimpleSlider.SWIPE_THRESHOLD) {
        this._direction = 'prev';
        this._move();
      } else {
        this._direction = 'none';
        this._move();
      }
      this._hasSwipeState = false;
    }

    function onDragStart(e) {
      e.preventDefault();
    }

    // click
    this._el.addEventListener('click', onClick.bind(this));

    // swipe
    if (this._config.swipe) {
      const options = ItcSimpleSlider.checkSupportPassiveEvents() ? { passive: false } : false;
      this._el.addEventListener('touchstart', onSwipeStart.bind(this), options);
      this._el.addEventListener('touchmove', onSwipeMove.bind(this), options);
      this._el.addEventListener('mousedown', onSwipeStart.bind(this));
      this._el.addEventListener('mousemove', onSwipeMove.bind(this));
      document.addEventListener('touchend', onSwipeEnd.bind(this));
      document.addEventListener('mouseup', onSwipeEnd.bind(this));
      document.addEventListener('mouseout', onSwipeEnd.bind(this));
    }
    this._el.addEventListener('dragstart', onDragStart.bind(this));

    function onResizeObserver(entries) {
      const contentBoxSize = entries[0].contentBoxSize;
      const contentRect = entries[0].contentRect;
      const newWidth = contentRect ? contentRect.width : (contentBoxSize[0] || contentBoxSize).inlineSize;
      let newTranslateX;
      if (this._width.toFixed(1) === newWidth.toFixed(1)) {
        return;
      }
      this._elItems.classList.add(ItcSimpleSlider.TRANSITION_NONE);
      this._width = parseInt(newWidth.toFixed(1), 10);
      newTranslateX = newWidth * parseInt(this._elItems.dataset.translate, 10);
      this._elItems.style.transform = `translateX(${newTranslateX}px)`;
      const $items2 = this._elsItem;
      for (let i = 0; i < $items2.length; i++) {
        const translateX = parseInt($items2[i].dataset.translate, 10);
        newTranslateX = translateX * newWidth;
        $items2[i].style.transform = `translateX(${newTranslateX}px)`;
      }
    }
    if (this._supportResizeObserver) {
      const resizeObserver = new ResizeObserver(onResizeObserver.bind(this));
      resizeObserver.observe(this._elWrapper);
    }
  }

  next() {
    this._direction = 'next';
    this._move();
  }
  prev() {
    this._direction = 'prev';
    this._move();
  }
  moveTo(index, useTransition) {
    this._moveTo(index, useTransition);
  }
}

document.addEventListener('DOMContentLoaded', function () {
  // Инициализация слайдера.
  const sliders = document.querySelectorAll('.js-slider');
  sliders.forEach(slider => {
    new ItcSimpleSlider(slider, {
      indicators: true,
      swipe: true,
    });
  });

  // Фильтрация.
  const searchInput = document.querySelector('.js-search');
  const groupList = document.querySelectorAll('.js-component-group');
  const componentsList = document.querySelector('.js-components-list');
  const components = componentsList.querySelectorAll('.js-component');
  searchInput.addEventListener('input', () => {
    const searchText = searchInput.value.toLowerCase().trim();

    // Скрываем компоненты.
    components.forEach(component => {
      if (searchText == '') {
        component.classList.remove('component-hidden');
        return;
      }

      if (component.textContent.toLowerCase().trim().includes(searchText)) {
        component.classList.remove('component-hidden');
      } else {
        component.classList.add('component-hidden');
      }
    });

    // Скрываем пустые группы.
    groupList.forEach(group => {
      if (!group.querySelector('.js-component:not(.component-hidden)')) {
        group.classList.add('component-hidden');
      } else {
        group.classList.remove('component-hidden');
      }
    })
  })

  // Кнопка сохранить у выбранной опции.
  const submitInput = document.querySelector('.submit-row input');
  let prevInput = null;
  components.forEach(component => {
    const input = component.querySelector('input[type=radio]');
    input.addEventListener('input', () => {
      prevInput?.remove();
      prevInput = submitInput.cloneNode(true);
      component.appendChild(prevInput)
    })

    if (input.getAttribute('checked') != null) {
      input.dispatchEvent(new CustomEvent('input'));
    }
  })
});
