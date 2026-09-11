/**
 * Kisan Web Project - AI Crop Leaf Disease Diagnostic Tool
 * Manages image drag-and-drop, laser scanning animation, REST diagnostic inference,
 * severity metrics, organic/chemical treatments, and embedded YouTube remedy tutorials.
 */

(function () {
  'use strict';

  let selectedFile = null;

  function initAIDiagnostics() {
    const dropzone = document.getElementById('ai-dropzone');
    const fileInput = document.getElementById('ai-file-input');
    const analyzeBtn = document.getElementById('ai-analyze-btn');
    const previewContainer = document.getElementById('ai-preview-container');
    const previewImg = document.getElementById('ai-preview-img');
    const scannerBox = document.getElementById('ai-scanner-box');
    const resultCard = document.getElementById('ai-result-card');

    if (!dropzone || !fileInput) return;

    // Drag & Drop events
    ['dragenter', 'dragover'].forEach((eventName) => {
      dropzone.addEventListener(eventName, (e) => {
        e.preventDefault();
        e.stopPropagation();
        dropzone.classList.add('border-emerald-400', 'bg-emerald-950/30');
      });
    });

    ['dragleave', 'drop'].forEach((eventName) => {
      dropzone.addEventListener(eventName, (e) => {
        e.preventDefault();
        e.stopPropagation();
        dropzone.classList.remove('border-emerald-400', 'bg-emerald-950/30');
      });
    });

    dropzone.addEventListener('drop', (e) => {
      const dt = e.dataTransfer;
      const files = dt.files;
      if (files.length > 0) {
        handleFileSelection(files[0]);
      }
    });

    fileInput.addEventListener('change', (e) => {
      if (e.target.files.length > 0) {
        handleFileSelection(e.target.files[0]);
      }
    });

    if (analyzeBtn) {
      analyzeBtn.addEventListener('click', () => {
        if (!selectedFile) {
          showToast('Please select or drag-and-drop a crop leaf image first.', 'warning');
          return;
        }
        performScanAnalysis(selectedFile);
      });
    }

    // Sample leaf quick test buttons
    const sampleButtons = document.querySelectorAll('.ai-sample-btn');
    sampleButtons.forEach((btn) => {
      btn.addEventListener('click', async () => {
        const sampleUrl = btn.dataset.url;
        const cropName = btn.dataset.crop || 'Tomato';
        try {
          btn.textContent = 'Loading sample...';
          const resp = await fetch(sampleUrl);
          const blob = await resp.blob();
          const file = new File([blob], `sample_${cropName.toLowerCase()}.jpg`, { type: 'image/jpeg' });
          handleFileSelection(file);
          btn.textContent = `Try: ${cropName}`;
          performScanAnalysis(file);
        } catch (err) {
          console.error('Error loading sample image:', err);
          btn.textContent = `Try: ${cropName}`;
        }
      });
    });
  }

  function handleFileSelection(file) {
    if (!file.type.startsWith('image/')) {
      showToast('Please upload a valid image file (PNG, JPG, WEBP).', 'error');
      return;
    }

    selectedFile = file;
    const previewContainer = document.getElementById('ai-preview-container');
    const previewImg = document.getElementById('ai-preview-img');
    const dropzonePlaceholder = document.getElementById('ai-dropzone-placeholder');
    const analyzeBtn = document.getElementById('ai-analyze-btn');

    const reader = new FileReader();
    reader.onload = (e) => {
      if (previewImg) previewImg.src = e.target.result;
      if (previewContainer) previewContainer.classList.remove('hidden');
      if (dropzonePlaceholder) dropzonePlaceholder.classList.add('hidden');
      if (analyzeBtn) {
        analyzeBtn.disabled = false;
        analyzeBtn.classList.remove('opacity-50', 'cursor-not-allowed');
      }
    };
    reader.readAsDataURL(file);
  }

  async function performScanAnalysis(file) {
    const scannerBox = document.getElementById('ai-scanner-box');
    const analyzeBtn = document.getElementById('ai-analyze-btn');
    const resultCard = document.getElementById('ai-result-card');
    const scanStatus = document.getElementById('ai-scan-status');

    if (scannerBox) scannerBox.classList.add('scanning');
    if (analyzeBtn) {
      analyzeBtn.disabled = true;
      analyzeBtn.innerHTML = `
        <svg class="animate-spin -ml-1 mr-2 h-4 w-4 text-white" fill="none" viewBox="0 0 24 24">
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
        </svg>
        Analyzing Neural Feature Maps...
      `;
    }
    if (scanStatus) scanStatus.textContent = 'Extracting chlorophyll & spectral lesion vectors...';

    const formData = new FormData();
    formData.append('image', file);
    formData.append('crop_name', 'Diagnosed Specimen');

    try {
      const resp = await fetch('/api/ai/diagnose', {
        method: 'POST',
        body: formData,
      });

      const data = await resp.json();

      setTimeout(() => {
        if (scannerBox) scannerBox.classList.remove('scanning');
        if (analyzeBtn) {
          analyzeBtn.disabled = false;
          analyzeBtn.innerHTML = 'Scan Another Specimen';
        }
        if (scanStatus) scanStatus.textContent = 'Diagnostic Complete';

        renderDiagnosticReport(data);
      }, 1200); // Cinematic scan delay
    } catch (err) {
      console.error('Diagnostic error:', err);
      if (scannerBox) scannerBox.classList.remove('scanning');
      if (analyzeBtn) {
        analyzeBtn.disabled = false;
        analyzeBtn.innerHTML = 'Analyze Leaf Specimen';
      }
      showToast('Network error analyzing leaf specimen. Please retry.', 'error');
    }
  }

  function renderDiagnosticReport(data) {
    const resultCard = document.getElementById('ai-result-card');
    if (!resultCard) return;

    const diseaseNameEl = document.getElementById('diag-disease-name');
    const cropNameEl = document.getElementById('diag-crop-name');
    const confidenceEl = document.getElementById('diag-confidence');
    const confidenceBarEl = document.getElementById('diag-confidence-bar');
    const severityBadgeEl = document.getElementById('diag-severity-badge');
    const symptomsListEl = document.getElementById('diag-symptoms-list');
    const organicTreatmentEl = document.getElementById('diag-organic-treatment');
    const chemicalTreatmentEl = document.getElementById('diag-chemical-treatment');
    const videoIframeEl = document.getElementById('diag-youtube-iframe');

    if (diseaseNameEl) diseaseNameEl.textContent = data.disease_name;
    if (cropNameEl) cropNameEl.textContent = `Host Crop: ${data.crop_name}`;
    if (confidenceEl) confidenceEl.textContent = `${data.confidence}% Confidence`;
    if (confidenceBarEl) confidenceBarEl.style.width = `${Math.min(100, data.confidence)}%`;

    // Severity styling
    if (severityBadgeEl) {
      severityBadgeEl.textContent = `${data.severity} Severity`;
      severityBadgeEl.className = 'px-3 py-1 text-xs font-bold rounded-full uppercase tracking-wider ';
      if (data.severity === 'Critical') {
        severityBadgeEl.classList.add('bg-red-500/20', 'text-red-400', 'border', 'border-red-500/40');
      } else if (data.severity === 'High') {
        severityBadgeEl.classList.add('bg-orange-500/20', 'text-orange-400', 'border', 'border-orange-500/40');
      } else if (data.severity === 'Medium') {
        severityBadgeEl.classList.add('bg-amber-500/20', 'text-amber-400', 'border', 'border-amber-500/40');
      } else {
        severityBadgeEl.classList.add('bg-emerald-500/20', 'text-emerald-400', 'border', 'border-emerald-500/40');
      }
    }

    // Symptoms
    if (symptomsListEl && data.symptoms) {
      symptomsListEl.innerHTML = '';
      data.symptoms.forEach((symptom) => {
        const li = document.createElement('li');
        li.className = 'flex items-start gap-2 text-xs text-slate-300';
        li.innerHTML = `
          <svg class="w-4 h-4 text-emerald-400 shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
          <span>${symptom}</span>
        `;
        symptomsListEl.appendChild(li);
      });
    }

    if (organicTreatmentEl) organicTreatmentEl.textContent = data.organic_treatment;
    if (chemicalTreatmentEl) chemicalTreatmentEl.textContent = data.chemical_treatment;

    // Embedded YouTube tutorial video
    if (videoIframeEl && data.youtube_tutorial_id) {
      videoIframeEl.src = `https://www.youtube.com/embed/${data.youtube_tutorial_id}`;
    }

    resultCard.classList.remove('hidden');
    resultCard.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
  }

  function showToast(message, type = 'info') {
    const toast = document.createElement('div');
    toast.className = `fixed bottom-6 right-6 z-50 px-4 py-3 rounded-xl shadow-2xl backdrop-blur-md border text-sm font-medium flex items-center gap-3 transform transition-all duration-300 translate-y-10 opacity-0 ${
      type === 'error'
        ? 'bg-red-950/90 text-red-200 border-red-500/30'
        : type === 'warning'
        ? 'bg-amber-950/90 text-amber-200 border-amber-500/30'
        : 'bg-emerald-950/90 text-emerald-200 border-emerald-500/30'
    }`;

    toast.innerHTML = `
      <svg class="w-5 h-5 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
      <span>${message}</span>
    `;

    document.body.appendChild(toast);
    setTimeout(() => {
      toast.classList.remove('translate-y-10', 'opacity-0');
    }, 50);

    setTimeout(() => {
      toast.classList.add('translate-y-10', 'opacity-0');
      setTimeout(() => toast.remove(), 300);
    }, 4000);
  }

  // Expose globally
  window.showToast = showToast;

  document.addEventListener('DOMContentLoaded', initAIDiagnostics);
})();
