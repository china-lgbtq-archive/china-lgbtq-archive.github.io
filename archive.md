---
layout: default
title: 档案库
permalink: /archive/
---

<div class="archive-page">
  
  <div class="archive-filters">
    <div class="search-box">
      <input type="text" id="search-input" placeholder="搜索档案...">
    </div>
    
    <div class="filter-row">
      <div class="filter-group">
        <span class="filter-label">年份</span>
        <div class="filter-tags" id="year-filters">
          {% assign all_years = "" | split: "" %}
          {% for entry in site.entries %}
            {% assign entry_year = entry.date | date: '%Y' %}
            {% unless all_years contains entry_year %}
              {% assign all_years = all_years | push: entry_year %}
            {% endunless %}
          {% endfor %}
          {% assign sorted_years = all_years | sort | reverse %}
          {% for year in sorted_years %}
          <button class="filter-btn" data-year="{{ year }}">{{ year }}</button>
          {% endfor %}
        </div>
      </div>
      
      <div class="filter-group">
        <span class="filter-label">标签</span>
        <div class="filter-tags" id="tag-filters">
          {% assign all_tags = site.entries | map: 'tags' | join: ',' | split: ',' | uniq | sort %}
          {% for tag in all_tags %}
          {% if tag != '' %}
          <button class="filter-btn" data-tag="{{ tag }}">{{ tag }}</button>
          {% endif %}
          {% endfor %}
        </div>
      </div>
    </div>
  </div>

  {% assign sorted_entries = site.entries | sort: 'date' | reverse %}
  
  <table class="archive-table" id="archive-list">
    <thead>
      <tr>
        <th class="col-date">日期</th>
        <th class="col-title">标题</th>
        <th class="col-tags">标签</th>
      </tr>
    </thead>
    <tbody>
      {% for entry in sorted_entries %}
      <tr class="archive-row" data-year="{{ entry.date | date: '%Y' }}" data-tags="{{ entry.tags | join: ',' }}" data-title="{{ entry.title }}" data-summary="{{ entry.summary }}" onclick="window.location='{{ entry.url | relative_url }}'">
        <td class="col-date">{{ entry.date | date: "%Y-%m-%d" }}</td>
        <td class="col-title">{{ entry.title }}</td>
        <td class="col-tags">
          <div class="tags-wrapper">
            {% if entry.tags %}
            {% for tag in entry.tags %}
            <a href="{{ '/archive/?tag=' | append: tag | relative_url }}" class="archive-tag" onclick="event.stopPropagation()">{{ tag }}</a>
            {% endfor %}
            {% endif %}
          </div>
        </td>
      </tr>
      {% endfor %}
    </tbody>
  </table>
  
  <div class="no-results" id="no-results" style="display: none;">
    没有找到匹配的档案
  </div>

</div>

<script>
document.addEventListener('DOMContentLoaded', function() {
  const searchInput = document.getElementById('search-input');
  const yearBtns = document.querySelectorAll('[data-year]');
  const tagBtns = document.querySelectorAll('[data-tag]');
  const rows = document.querySelectorAll('.archive-row');
  const noResults = document.getElementById('no-results');
  
  let currentYear = null;
  let currentTag = null;
  let currentSearch = '';
  
  function filterItems() {
    let visibleCount = 0;
    
    rows.forEach(row => {
      const year = row.dataset.year;
      const title = row.dataset.title.toLowerCase();
      const summary = row.dataset.summary.toLowerCase();
      const tags = row.dataset.tags.toLowerCase();
      
      const matchYear = !currentYear || year === currentYear;
      const matchTag = !currentTag || tags.includes(currentTag.toLowerCase());
      const matchSearch = currentSearch === '' || 
        title.includes(currentSearch) || 
        summary.includes(currentSearch) ||
        tags.includes(currentSearch);
      
      if (matchYear && matchTag && matchSearch) {
        row.style.display = '';
        visibleCount++;
      } else {
        row.style.display = 'none';
      }
    });
    
    noResults.style.display = visibleCount === 0 ? '' : 'none';
    updateURL();
  }
  
  function updateURL() {
    const params = new URLSearchParams();
    if (currentYear) params.set('year', currentYear);
    if (currentTag) params.set('tag', currentTag);
    if (currentSearch) params.set('q', currentSearch);
    
    const newURL = params.toString() 
      ? window.location.pathname + '?' + params.toString()
      : window.location.pathname;
    history.replaceState(null, '', newURL);
  }
  
  function loadFromURL() {
    const params = new URLSearchParams(window.location.search);
    
    if (params.has('year')) {
      currentYear = params.get('year');
      yearBtns.forEach(b => {
        if (b.dataset.year === currentYear) b.classList.add('active');
      });
    }
    
    if (params.has('tag')) {
      currentTag = params.get('tag');
      tagBtns.forEach(b => {
        if (b.dataset.tag.toLowerCase() === currentTag.toLowerCase()) b.classList.add('active');
      });
    }
    
    if (params.has('q')) {
      currentSearch = params.get('q').toLowerCase();
      searchInput.value = params.get('q');
    }
    
    filterItems();
  }
  
  // 年份按钮：单选 toggle
  yearBtns.forEach(btn => {
    btn.addEventListener('click', function() {
      const year = this.dataset.year;
      
      if (currentYear === year) {
        // 已选中，取消选择
        currentYear = null;
        this.classList.remove('active');
      } else {
        // 选择新的，取消其他
        yearBtns.forEach(b => b.classList.remove('active'));
        currentYear = year;
        this.classList.add('active');
      }
      
      filterItems();
    });
  });
  
  // 标签按钮：单选 toggle
  tagBtns.forEach(btn => {
    btn.addEventListener('click', function() {
      const tag = this.dataset.tag;
      
      if (currentTag === tag.toLowerCase()) {
        // 已选中，取消选择
        currentTag = null;
        this.classList.remove('active');
      } else {
        // 选择新的，取消其他
        tagBtns.forEach(b => b.classList.remove('active'));
        currentTag = tag.toLowerCase();
        this.classList.add('active');
      }
      
      filterItems();
    });
  });
  
  searchInput.addEventListener('input', function() {
    currentSearch = this.value.toLowerCase();
    filterItems();
  });
  
  loadFromURL();
});
</script>
