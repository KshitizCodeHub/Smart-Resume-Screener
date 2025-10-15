// ===== Configuration =====
const API_BASE_URL = 'http://localhost:8000';

// ===== State Management =====
const state = {
    resumes: [],
    jobs: [],
    currentTab: 'upload',
    theme: localStorage.getItem('theme') || 'light',
    currentMatchResults: null  // Store match results for theme switching
};

// ===== Initialization =====
document.addEventListener('DOMContentLoaded', () => {
    initializeApp();
});

function initializeApp() {
    initializeTheme();
    setupEventListeners();
    loadResumes();
    loadJobs();
}

// ===== Theme Management =====
function initializeTheme() {
    document.documentElement.setAttribute('data-theme', state.theme);
}

function toggleTheme() {
    state.theme = state.theme === 'light' ? 'dark' : 'light';
    document.documentElement.setAttribute('data-theme', state.theme);
    localStorage.setItem('theme', state.theme);
    
    // Animate the toggle button
    const toggleBtn = document.getElementById('theme-toggle');
    toggleBtn.style.transform = 'rotate(360deg)';
    setTimeout(() => {
        toggleBtn.style.transform = 'rotate(0deg)';
    }, 300);
    
    // CRITICAL: Regenerate charts with new theme colors
    // Only regenerate if we have match results displayed
    if (state.currentMatchResults && state.currentMatchResults.length > 0) {
        console.log('Theme changed - regenerating charts with new colors');
        generateAnalytics(state.currentMatchResults);
    }
}

// ===== Event Listeners =====
function setupEventListeners() {
    // Tab navigation
    document.querySelectorAll('.nav-btn').forEach(btn => {
        btn.addEventListener('click', (e) => switchTab(e.target.dataset.tab));
    });

    // Theme toggle
    document.getElementById('theme-toggle').addEventListener('click', toggleTheme);

    // Resume upload
    const resumeUploadArea = document.getElementById('resume-upload-area');
    const resumeFileInput = document.getElementById('resume-file-input');
    
    resumeUploadArea.addEventListener('click', () => resumeFileInput.click());
    resumeUploadArea.addEventListener('dragover', handleDragOver);
    resumeUploadArea.addEventListener('drop', handleResumeDrop);
    resumeFileInput.addEventListener('change', handleResumeFileSelect);

    // Job form
    document.getElementById('job-form').addEventListener('submit', handleJobSubmit);

    // Job selector
    document.getElementById('job-select').addEventListener('change', (e) => {
        const btn = document.getElementById('start-matching-btn');
        btn.disabled = !e.target.value;
    });

    // Start matching
    document.getElementById('start-matching-btn').addEventListener('click', startMatching);
}

// ===== Tab Switching =====
function switchTab(tabName) {
    // Update nav buttons
    document.querySelectorAll('.nav-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    document.querySelector(`[data-tab="${tabName}"]`).classList.add('active');

    // Update tab content
    document.querySelectorAll('.tab-content').forEach(content => {
        content.classList.remove('active');
    });
    document.getElementById(`${tabName}-tab`).classList.add('active');

    state.currentTab = tabName;

    // Load data when switching to dashboard or match tab
    if (tabName === 'dashboard') {
        loadResumes();
        loadJobs();
    } else if (tabName === 'match') {
        populateJobSelector();
    }
}

// ===== Resume Upload =====
function handleDragOver(e) {
    e.preventDefault();
    e.currentTarget.style.borderColor = 'var(--primary-color)';
}

function handleResumeDrop(e) {
    e.preventDefault();
    e.currentTarget.style.borderColor = '';
    const file = e.dataTransfer.files[0];
    if (file) uploadResume(file);
}

function handleResumeFileSelect(e) {
    const file = e.target.files[0];
    if (file) uploadResume(file);
}

async function uploadResume(file) {
    // Validate file
    const validTypes = ['.pdf', '.docx', '.txt'];
    const fileExt = '.' + file.name.split('.').pop().toLowerCase();
    
    if (!validTypes.includes(fileExt)) {
        showToast('Please upload PDF, DOCX, or TXT file', 'error');
        return;
    }

    if (file.size > 10 * 1024 * 1024) {
        showToast('File size must be less than 10MB', 'error');
        return;
    }

    // Show progress
    const progressEl = document.getElementById('resume-upload-progress');
    const resultEl = document.getElementById('resume-upload-result');
    progressEl.classList.remove('hidden');
    resultEl.classList.add('hidden');

    // Upload file
    const formData = new FormData();
    formData.append('file', file);

    try {
        const response = await fetch(`${API_BASE_URL}/api/upload-resume`, {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        if (response.ok) {
            // Extract just success message without ID
            const cleanMessage = data.message.split('.')[0]; // Get text before ID
            showResult(resultEl, `✓ Resume uploaded and parsed successfully!`, 'success');
            showToast('Resume uploaded successfully!', 'success');
            loadResumes();
        } else {
            showResult(resultEl, `✗ ${data.detail || 'Upload failed'}`, 'error');
            showToast('Upload failed', 'error');
        }
    } catch (error) {
        showResult(resultEl, `✗ Network error: ${error.message}`, 'error');
        showToast('Network error', 'error');
    } finally {
        progressEl.classList.add('hidden');
    }
}

// ===== Job Creation =====
async function handleJobSubmit(e) {
    e.preventDefault();

    const title = document.getElementById('job-title').value.trim();
    const description = document.getElementById('job-description').value.trim();

    if (!title || !description) {
        showToast('Please fill in all fields', 'error');
        return;
    }

    const resultEl = document.getElementById('job-upload-result');
    resultEl.classList.add('hidden');

    try {
        const response = await fetch(`${API_BASE_URL}/api/upload-job`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                title,
                description,
                requirements: []
            })
        });

        const data = await response.json();

        if (response.ok) {
            showResult(resultEl, `✓ Job description created successfully!`, 'success');
            showToast('Job created successfully!', 'success');
            e.target.reset();
            loadJobs();
        } else {
            showResult(resultEl, `✗ ${data.detail || 'Failed to create job'}`, 'error');
            showToast('Failed to create job', 'error');
        }
    } catch (error) {
        showResult(resultEl, `✗ Network error: ${error.message}`, 'error');
        showToast('Network error', 'error');
    }
}

// ===== Load Resumes =====
async function loadResumes() {
    const listEl = document.getElementById('resumes-list');
    listEl.innerHTML = '<div class="loading"><i class="fas fa-spinner fa-spin"></i> Loading...</div>';

    try {
        const response = await fetch(`${API_BASE_URL}/api/resumes`);
        const data = await response.json();

        state.resumes = data.resumes || [];

        if (state.resumes.length === 0) {
            listEl.innerHTML = `
                <div class="empty-state">
                    <i class="fas fa-file-alt"></i>
                    <p>No resumes uploaded yet</p>
                </div>
            `;
            return;
        }

        listEl.innerHTML = state.resumes.map(resume => createResumeCard(resume)).join('');
    } catch (error) {
        listEl.innerHTML = `
            <div class="empty-state">
                <i class="fas fa-exclamation-circle"></i>
                <p>Error loading resumes</p>
            </div>
        `;
    }
}

function createResumeCard(resume) {
    const parsed = resume.parsed_data || {};
    const name = parsed.name || 'Unknown Candidate';
    const email = parsed.email || 'No email';
    const skills = parsed.skills?.slice(0, 3) || [];
    const date = new Date(resume.upload_date).toLocaleDateString();

    return `
        <div class="item-card" onclick='viewResumeDetails(${JSON.stringify(resume).replace(/'/g, "&apos;")})'>
            <div class="item-header">
                <div>
                    <div class="item-title">${name}</div>
                    <div style="font-size: 13px; color: var(--text-secondary); margin-top: 4px;">
                        ${email}
                    </div>
                </div>
                <div class="item-date">${date}</div>
            </div>
            <div class="item-meta">
                ${skills.map(skill => `<span class="tag">${skill}</span>`).join('')}
                ${skills.length > 0 ? '' : '<span class="tag">No skills extracted</span>'}
                <button class="btn-delete" onclick="event.stopPropagation(); deleteResume('${resume._id}')">
                    <i class="fas fa-trash"></i> Delete
                </button>
            </div>
        </div>
    `;
}

// ===== Load Jobs =====
async function loadJobs() {
    const listEl = document.getElementById('jobs-list');
    listEl.innerHTML = '<div class="loading"><i class="fas fa-spinner fa-spin"></i> Loading...</div>';

    try {
        const response = await fetch(`${API_BASE_URL}/api/jobs`);
        const data = await response.json();

        state.jobs = data.jobs || [];

        if (state.jobs.length === 0) {
            listEl.innerHTML = `
                <div class="empty-state">
                    <i class="fas fa-briefcase"></i>
                    <p>No job descriptions yet</p>
                </div>
            `;
            return;
        }

        listEl.innerHTML = state.jobs.map(job => createJobCard(job)).join('');
    } catch (error) {
        listEl.innerHTML = `
            <div class="empty-state">
                <i class="fas fa-exclamation-circle"></i>
                <p>Error loading jobs</p>
            </div>
        `;
    }
}

function createJobCard(job) {
    const date = new Date(job.created_date).toLocaleDateString();
    const descriptionPreview = job.description.slice(0, 150) + '...';

    return `
        <div class="item-card" style="cursor: pointer;" onclick='viewJobDetails(${JSON.stringify(job)})'>
            <div class="item-header">
                <div>
                    <div class="item-title">${job.title}</div>
                    <p style="font-size: 13px; color: var(--text-secondary); margin-top: 8px;">
                        ${descriptionPreview}
                    </p>
                </div>
                <div class="item-date">${date}</div>
            </div>
            <button class="btn-delete" onclick="event.stopPropagation(); deleteJob('${job._id}')">
                <i class="fas fa-trash"></i> Delete
            </button>
        </div>
    `;
}

// ===== Delete Operations =====
async function deleteResume(id) {
    if (!confirm('Are you sure you want to delete this resume?')) return;

    try {
        const response = await fetch(`${API_BASE_URL}/api/resumes/${id}`, {
            method: 'DELETE'
        });

        if (response.ok) {
            showToast('Resume deleted', 'success');
            loadResumes();
        } else {
            showToast('Failed to delete resume', 'error');
        }
    } catch (error) {
        showToast('Network error', 'error');
    }
}

async function deleteJob(id) {
    if (!confirm('Are you sure you want to delete this job?')) return;

    try {
        const response = await fetch(`${API_BASE_URL}/api/jobs/${id}`, {
            method: 'DELETE'
        });

        if (response.ok) {
            showToast('Job deleted', 'success');
            loadJobs();
        } else {
            showToast('Failed to delete job', 'error');
        }
    } catch (error) {
        showToast('Network error', 'error');
    }
}

// ===== Matching =====
function populateJobSelector() {
    const select = document.getElementById('job-select');
    select.innerHTML = '<option value="">Choose a job description...</option>';

    state.jobs.forEach(job => {
        const option = document.createElement('option');
        option.value = job._id;
        option.textContent = job.title;
        select.appendChild(option);
    });
}

async function startMatching() {
    const jobId = document.getElementById('job-select').value;
    if (!jobId) return;

    const progressEl = document.getElementById('matching-progress');
    const resultsEl = document.getElementById('match-results');

    progressEl.classList.remove('hidden');
    resultsEl.classList.add('hidden');

    try {
        const response = await fetch(`${API_BASE_URL}/api/match`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ job_id: jobId })
        });

        const data = await response.json();

        if (response.ok) {
            displayMatchResults(data);
            showToast('Matching completed!', 'success');
        } else {
            showToast('Matching failed', 'error');
        }
    } catch (error) {
        showToast('Network error', 'error');
    } finally {
        progressEl.classList.add('hidden');
    }
}

function displayMatchResults(data) {
    const resultsEl = document.getElementById('match-results');
    const countEl = document.getElementById('results-count');
    const tableContainer = document.getElementById('results-table-container');
    const analyticsSection = document.getElementById('analytics-section');

    const matches = data.matches || [];
    
    // Store match results in state for theme switching
    state.currentMatchResults = matches;
    
    countEl.textContent = `${matches.length} candidate${matches.length !== 1 ? 's' : ''} found`;

    if (matches.length === 0) {
        tableContainer.innerHTML = `
            <div class="empty-state">
                <i class="fas fa-search"></i>
                <p>No matches found</p>
            </div>
        `;
        analyticsSection.classList.add('hidden');
    } else {
        // Show loading state for analytics
        analyticsSection.classList.remove('hidden');
        analyticsSection.innerHTML = `
            <h3 class="analytics-title">
                <i class="fas fa-chart-pie"></i> Match Analytics
            </h3>
            <div class="analytics-loading" style="text-align:center;padding:60px 20px;">
                <div class="spinner" style="width:50px;height:50px;border:4px solid var(--border-light);border-top-color:var(--primary-color);border-radius:50%;animation:spin 1s linear infinite;margin:0 auto 20px;"></div>
                <p style="color:var(--text-secondary);font-size:14px;">Generating analytics...</p>
            </div>
        `;
        
        // Generate visual analytics with slight delay for UI feedback
        setTimeout(() => {
            try {
                generateAnalytics(matches);
            } catch (error) {
                console.error('Failed to generate analytics:', error);
                analyticsSection.innerHTML = `
                    <h3 class="analytics-title">
                        <i class="fas fa-chart-pie"></i> Match Analytics
                    </h3>
                    <div style="text-align:center;padding:60px 20px;color:var(--danger-color);">
                        <i class="fas fa-exclamation-triangle" style="font-size:48px;margin-bottom:16px;opacity:0.7;"></i>
                        <p style="font-size:16px;font-weight:600;margin-bottom:8px;">Could not load analytics</p>
                        <p style="font-size:13px;opacity:0.7;">Please try refreshing the page</p>
                    </div>
                `;
            }
        }, 300);
        
        tableContainer.innerHTML = `
            <table class="results-table">
                <thead>
                    <tr>
                        <th>Candidate</th>
                        <th>Score</th>
                        <th>Justification</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    ${matches.map((match, index) => createMatchRow(match, index)).join('')}
                </tbody>
            </table>
        `;
    }

    resultsEl.classList.remove('hidden');
}

function createMatchRow(match, index) {
    const score = match.score || 0;
    const scoreClass = score >= 7 ? 'high' : score >= 5 ? 'medium' : 'low';
    const justification = (match.justification || '').slice(0, 100) + '...';
    
    // Smart score display: show decimal only if needed
    const scoreDisplay = (score % 1 === 0) ? `${score}/10` : `${score.toFixed(1)}/10`;

    return `
        <tr>
            <td>
                <div style="font-weight: 600;">${match.candidate_name || 'Unknown'}</div>
                <div style="font-size: 12px; color: var(--text-secondary);">${match.resume_filename || ''}</div>
            </td>
            <td>
                <span class="score-badge ${scoreClass}">
                    ${scoreDisplay}
                </span>
            </td>
            <td style="max-width: 300px;">
                ${justification}
            </td>
            <td>
                <button class="expand-btn" onclick="toggleMatchDetails(${index})">
                    <i class="fas fa-chevron-down"></i> Details
                </button>
            </td>
        </tr>
        <tr id="details-${index}" class="hidden">
            <td colspan="4">
                ${createMatchDetails(match)}
            </td>
        </tr>
    `;
}

// Helper function to decode HTML entities and format markdown-style bold
function decodeHTML(html) {
    const txt = document.createElement('textarea');
    txt.innerHTML = html;
    let decoded = txt.value;
    
    // Convert **text** to <strong>text</strong> for bold formatting
    decoded = decoded.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');
    
    return decoded;
}

function createMatchDetails(match) {
    const matchingPoints = match.matching_points || [];
    const missingQuals = match.missing_qualifications || [];
    const strengths = match.strengths || [];

    return `
        <div class="match-details">
            <div class="detail-section">
                <h4><i class="fas fa-check-circle" style="color: var(--success-color);"></i> Matching Points</h4>
                <ul>
                    ${matchingPoints.map(point => `<li>${decodeHTML(point)}</li>`).join('') || '<li>None specified</li>'}
                </ul>
            </div>
            <div class="detail-section">
                <h4><i class="fas fa-star" style="color: var(--warning-color);"></i> Strengths</h4>
                <ul>
                    ${strengths.map(strength => `<li>${decodeHTML(strength)}</li>`).join('') || '<li>None specified</li>'}
                </ul>
            </div>
            <div class="detail-section">
                <h4><i class="fas fa-exclamation-triangle" style="color: var(--danger-color);"></i> Missing Qualifications</h4>
                <ul>
                    ${missingQuals.map(qual => `<li>${decodeHTML(qual)}</li>`).join('') || '<li>None</li>'}
                </ul>
            </div>
            <div class="detail-section">
                <h4><i class="fas fa-comment"></i> Full Justification</h4>
                <div style="color: var(--text-secondary); line-height: 1.8; white-space: pre-line;">
                    ${formatJustification(decodeHTML(match.justification || 'No justification provided'))}
                </div>
            </div>
        </div>
    `;
}

// Helper function to format justification text
function formatJustification(text) {
    if (!text) return '';
    
    console.log('=== JUSTIFICATION DEBUG ===');
    console.log('Original text:', text.substring(0, 300));
    
    // First, clean up excessive whitespace
    text = text.replace(/\s+/g, ' ').trim();
    
    // Bold ALL score patterns - more comprehensive
    // Match: (X.X/Y.Y), (X.X/Y), (X/Y.Y), (X/Y), X.X/Y.Y, X.X/Y, X/Y
    
    // In parentheses with decimals: (1.5/1.5), (4.0/4), (1.5/3), (4/4)
    text = text.replace(/\((\d+\.\d+)\/(\d+\.\d+)\)/g, '(<strong>$1/$2</strong>)');
    text = text.replace(/\((\d+)\.0\/(\d+\.?\d*)\)/g, '(<strong>$1/$2</strong>)');
    text = text.replace(/\((\d+\.\d+)\/(\d+)\)/g, '(<strong>$1/$2</strong>)');
    text = text.replace(/\((\d+)\/(\d+\.\d+)\)/g, '(<strong>$1/$2</strong>)');
    text = text.replace(/\((\d+)\/(\d+)\)/g, '(<strong>$1/$2</strong>)');
    
    // Without parentheses: 1.5/1.5, 4/4, etc.
    text = text.replace(/(\d+\.\d+)\/(\d+\.\d+)(?!<\/strong>)/g, '<strong>$1/$2</strong>');
    text = text.replace(/(\d+\.\d+)\/(\d+)(?!<\/strong>)/g, '<strong>$1/$2</strong>');
    text = text.replace(/(\d+)\/(\d+)(?!<\/strong>)/g, '<strong>$1/$2</strong>');
    
    console.log('After score bolding:', text.substring(0, 300));
    
    // Split by periods followed by capital letters
    let sentences = text.split(/(?<=\.)\s+(?=[A-Z])/);
    
    let formatted = '';
    let currentParagraph = [];
    
    sentences.forEach((sentence, index) => {
        sentence = sentence.trim();
        if (!sentence) return;
        
        // Check if this is a section header (ends with colon or is very short)
        const isHeader = sentence.endsWith(':') || (sentence.length < 80 && !sentence.endsWith('.'));
        
        // Check if starting a new topic (contains keywords)
        const startsNewTopic = /^(Additionally|Furthermore|Moreover|However|In addition|On the other hand)/i.test(sentence);
        
        if (isHeader) {
            // If we have a current paragraph, add it
            if (currentParagraph.length > 0) {
                formatted += currentParagraph.join(' ') + '\n\n';
                currentParagraph = [];
            }
            // Add header with extra spacing
            formatted += sentence + '\n';
        } else if (startsNewTopic && currentParagraph.length > 0) {
            // Start a new paragraph
            formatted += currentParagraph.join(' ') + '\n\n';
            currentParagraph = [sentence];
        } else {
            currentParagraph.push(sentence);
        }
        
        // Every 3-4 sentences, start a new paragraph
        if (currentParagraph.length >= 3 && !isHeader) {
            formatted += currentParagraph.join(' ') + '\n\n';
            currentParagraph = [];
        }
    });
    
    // Add any remaining paragraph
    if (currentParagraph.length > 0) {
        formatted += currentParagraph.join(' ');
    }
    
    return formatted.trim();
}

function toggleMatchDetails(index) {
    const detailsRow = document.getElementById(`details-${index}`);
    detailsRow.classList.toggle('hidden');
}

// ===== Resume Details Modal =====
function viewResumeDetails(resume) {
    const modal = document.getElementById('resume-modal');
    const modalBody = document.getElementById('modal-body');

    const parsed = resume.parsed_data || {};

    modalBody.innerHTML = `
        <div style="margin-bottom: 24px;">
            <h3 style="margin-bottom: 8px;">${parsed.name || 'Unknown Candidate'}</h3>
            <p style="color: var(--text-secondary);">${parsed.email || 'No email'}</p>
            <p style="color: var(--text-secondary);">${parsed.phone || 'No phone'}</p>
        </div>

        ${parsed.skills && parsed.skills.length > 0 ? `
            <div style="margin-bottom: 24px;">
                <h4 style="margin-bottom: 12px;">Skills</h4>
                <div style="display: flex; flex-wrap: wrap; gap: 8px;">
                    ${parsed.skills.map(skill => `<span class="tag">${skill}</span>`).join('')}
                </div>
            </div>
        ` : ''}

        ${parsed.experience && parsed.experience.length > 0 ? `
            <div style="margin-bottom: 24px;">
                <h4 style="margin-bottom: 12px;">Experience</h4>
                ${parsed.experience.map(exp => `
                    <div style="margin-bottom: 12px; padding: 12px; background: var(--bg-color); border-radius: 8px;">
                        <div style="font-weight: 600;">${exp.role || 'Role'}</div>
                        <div style="color: var(--text-secondary); font-size: 13px;">${exp.company || 'Company'} • ${exp.duration || 'Duration'}</div>
                    </div>
                `).join('')}
            </div>
        ` : ''}

        ${parsed.education && parsed.education.length > 0 ? `
            <div style="margin-bottom: 24px;">
                <h4 style="margin-bottom: 12px;">Education</h4>
                ${parsed.education.map(edu => `
                    <div style="margin-bottom: 12px; padding: 12px; background: var(--bg-color); border-radius: 8px;">
                        <div style="font-weight: 600;">${edu.degree || 'Degree'}</div>
                        <div style="color: var(--text-secondary); font-size: 13px;">${edu.institution || 'Institution'} • ${edu.year || 'Year'}</div>
                    </div>
                `).join('')}
            </div>
        ` : ''}
    `;

    modal.classList.remove('hidden');
}

function closeModal() {
    document.getElementById('resume-modal').classList.add('hidden');
}

// Click outside modal to close
document.getElementById('resume-modal').addEventListener('click', (e) => {
    if (e.target.id === 'resume-modal') {
        closeModal();
    }
});

// View job details in modal
function viewJobDetails(job) {
    const modal = document.getElementById('job-modal');
    const titleEl = document.getElementById('modal-job-title');
    const detailsEl = document.getElementById('modal-job-details');
    
    titleEl.textContent = job.title;
    
    let requirementsHTML = '';
    if (job.requirements && job.requirements.length > 0) {
        requirementsHTML = `
            <div class="detail-section">
                <h4><i class="fas fa-check-circle"></i> Requirements</h4>
                <ul class="requirements-list">
                    ${job.requirements.map(req => `<li>${req}</li>`).join('')}
                </ul>
            </div>
        `;
    }
    
    detailsEl.innerHTML = `
        <div class="detail-section">
            <h4><i class="fas fa-building"></i> Company</h4>
            <p>${job.company || 'Not specified'}</p>
        </div>
        <div class="detail-section">
            <h4><i class="fas fa-map-marker-alt"></i> Location</h4>
            <p>${job.location || 'Not specified'}</p>
        </div>
        <div class="detail-section">
            <h4><i class="fas fa-file-alt"></i> Description</h4>
            <p style="white-space: pre-line;">${job.description}</p>
        </div>
        ${requirementsHTML}
    `;
    
    modal.classList.remove('hidden');
}

function closeJobModal() {
    document.getElementById('job-modal').classList.add('hidden');
}

// Click outside job modal to close
document.getElementById('job-modal').addEventListener('click', (e) => {
    if (e.target.id === 'job-modal') {
        closeJobModal();
    }
});

// ===== Utility Functions =====
function showResult(element, message, type) {
    element.textContent = message;
    element.className = `upload-result ${type}`;
    element.classList.remove('hidden');
}

function showToast(message, type = 'success') {
    const toast = document.getElementById('toast');
    const toastMessage = document.getElementById('toast-message');
    
    toastMessage.textContent = message;
    toast.className = `toast ${type}`;
    toast.classList.remove('hidden');

    setTimeout(() => {
        toast.classList.add('hidden');
    }, 3000);
}

// ===== Visual Analytics =====
let scoreChart = null;
let skillsChart = null;

function generateAnalytics(matchResults) {
    console.log('=== ANALYTICS DEBUG ===');
    console.log('Match results received:', matchResults);
    console.log('Sample result:', matchResults && matchResults.length > 0 ? matchResults[0] : 'NONE');
    
    const analyticsSection = document.getElementById('analytics-section');
    
    // Safety check
    if (!matchResults || matchResults.length === 0) {
        console.log('No match results to display');
        analyticsSection.innerHTML = `
            <h3 class="analytics-title">
                <i class="fas fa-chart-pie"></i> Match Analytics
            </h3>
            <div style="text-align:center;padding:40px;color:var(--text-secondary);">
                <i class="fas fa-info-circle" style="font-size:48px;margin-bottom:16px;opacity:0.5;"></i>
                <p>No match data available</p>
            </div>
        `;
        analyticsSection.classList.remove('hidden');
        return;
    }
    
    // Restore the proper HTML structure if it was replaced
    analyticsSection.innerHTML = `
        <h3 class="analytics-title">
            <i class="fas fa-chart-pie"></i> Match Analytics
        </h3>
        <div class="analytics-grid">
            <!-- Score Distribution Chart -->
            <div class="analytics-card">
                <h4><i class="fas fa-chart-bar"></i> Score Distribution</h4>
                <canvas id="score-chart"></canvas>
            </div>
            
            <!-- Skills Match Chart -->
            <div class="analytics-card">
                <h4><i class="fas fa-bullseye"></i> Skills Match Overview</h4>
                <div class="chart-container">
                    <canvas id="skills-chart"></canvas>
                </div>
            </div>
            
            <!-- Top Candidates -->
            <div class="analytics-card">
                <h4><i class="fas fa-trophy"></i> Top Candidates</h4>
                <div id="top-candidates-list"></div>
            </div>
            
            <!-- Match Quality Metrics -->
            <div class="analytics-card">
                <h4><i class="fas fa-tachometer-alt"></i> Match Quality</h4>
                <div id="quality-metrics"></div>
            </div>
        </div>
    `;
    
    analyticsSection.classList.remove('hidden');
    
    // Convert score (0-10) to percentage (0-100) for consistency
    const scores = matchResults.map(r => {
        const score = r.score || r.match_score || 0;
        // If score is already 0-100, use it; if 0-10, convert to percentage
        return score <= 10 ? score * 10 : score;
    });
    const candidates = matchResults.map(r => r.candidate_name || 'Unknown');
    
    console.log('Converted scores:', scores);
    console.log('Candidates:', candidates);
    
    // Generate all visualizations with error handling
    try {
        generateScoreChart(scores, candidates);
        console.log('✓ Score chart generated');
    } catch (error) {
        console.error('✗ Error generating score chart:', error);
        const scoreCard = document.querySelector('#score-chart').closest('.analytics-card');
        if (scoreCard) {
            scoreCard.innerHTML = '<h4><i class="fas fa-chart-bar"></i> Score Distribution</h4><p style="text-align:center;padding:40px;color:var(--text-secondary);font-size:13px;">Unable to generate chart</p>';
        }
    }
    
    try {
        generateSkillsChart(matchResults);
        console.log('✓ Skills chart generated');
    } catch (error) {
        console.error('✗ Error generating skills chart:', error);
        const skillsContainer = document.querySelector('.chart-container');
        if (skillsContainer) {
            skillsContainer.innerHTML = '<p style="text-align:center;padding:40px;color:var(--text-secondary);font-size:13px;"><i class="fas fa-info-circle" style="display:block;font-size:32px;margin-bottom:12px;opacity:0.5;"></i>Unable to generate skills chart</p>';
        }
    }
    
    try {
        generateTopCandidates(matchResults);
        console.log('✓ Top candidates generated');
    } catch (error) {
        console.error('✗ Error generating top candidates:', error);
        const topCandidatesEl = document.getElementById('top-candidates-list');
        if (topCandidatesEl) {
            topCandidatesEl.innerHTML = '<p style="color:var(--text-secondary);text-align:center;padding:20px;font-size:13px;">Unable to load candidates</p>';
        }
    }
    
    try {
        generateQualityMetrics(matchResults);
        console.log('✓ Quality metrics generated');
    } catch (error) {
        console.error('✗ Error generating quality metrics:', error);
        const metricsEl = document.getElementById('quality-metrics');
        if (metricsEl) {
            metricsEl.innerHTML = '<p style="color:var(--text-secondary);text-align:center;padding:20px;font-size:13px;">Unable to load metrics</p>';
        }
    }
}

function generateScoreChart(scores, candidates) {
    const ctx = document.getElementById('score-chart');
    
    if (!ctx) {
        console.error('Score chart canvas not found');
        return;
    }
    
    // Destroy existing chart if it exists
    if (scoreChart) {
        scoreChart.destroy();
        scoreChart = null;
    }
    
    // Create score distribution data (scores should be 0-100)
    const scoreRanges = {
        'Excellent (80-100)': 0,
        'Good (60-79)': 0,
        'Average (40-59)': 0,
        'Below Average (0-39)': 0
    };
    
    scores.forEach(score => {
        if (score >= 80) scoreRanges['Excellent (80-100)']++;
        else if (score >= 60) scoreRanges['Good (60-79)']++;
        else if (score >= 40) scoreRanges['Average (40-59)']++;
        else scoreRanges['Below Average (0-39)']++;
    });
    
    // Get theme and set colors
    const htmlElement = document.documentElement;
    const theme = htmlElement.getAttribute('data-theme') || 'light';
    const isDark = theme === 'dark';
    
    // COSMETIC FIX: Ensure proper contrast in BOTH themes
    // Dark mode: Light text (#f1f5f9 = white-ish) for visibility
    // Light mode: Very dark text (#0f172a = near-black) for visibility
    const textColor = isDark ? '#f1f5f9' : '#0f172a';
    const gridColor = isDark ? 'rgba(148, 163, 184, 0.3)' : 'rgba(100, 116, 139, 0.2)';
    
    console.log('=== SCORE CHART DEBUG ===');
    console.log('Theme:', theme, '| isDark:', isDark);
    console.log('Text Color:', textColor, '(dark mode=#f1f5f9/white, light mode=#0f172a/black)');
    console.log('Score ranges:', scoreRanges);
    
    scoreChart = new Chart(ctx, {
        type: 'bar',
        data: {
            // Use SHORTER, COMPACT labels to prevent overlap
            labels: ['Excellent\n80-100', 'Good\n60-79', 'Average\n40-59', 'Below Avg\n0-39'],
            datasets: [{
                label: 'Number of Candidates',
                data: [
                    scoreRanges['Excellent (80-100)'],
                    scoreRanges['Good (60-79)'],
                    scoreRanges['Average (40-59)'],
                    scoreRanges['Below Average (0-39)']
                ],
                backgroundColor: [
                    'rgba(16, 185, 129, 0.8)',
                    'rgba(99, 102, 241, 0.8)',
                    'rgba(245, 158, 11, 0.8)',
                    'rgba(239, 68, 68, 0.8)'
                ],
                borderColor: [
                    'rgba(16, 185, 129, 1)',
                    'rgba(99, 102, 241, 1)',
                    'rgba(245, 158, 11, 1)',
                    'rgba(239, 68, 68, 1)'
                ],
                borderWidth: 2,
                borderRadius: 8,
                // COSMETIC FIX: Equal bar spacing
                barPercentage: 0.7,
                categoryPercentage: 0.9
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,  // LAYOUT FIX: Allow chart to fill full height
            layout: {
                padding: {
                    left: 8,      // Increased from 5 for better balance
                    right: 8,     // Increased from 5 for better balance
                    top: 15,      // Increased from 10 for more breathing room
                    bottom: 8     // Increased from 5 for better balance
                }
            },
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    backgroundColor: isDark ? 'rgba(30, 41, 59, 0.95)' : 'rgba(255, 255, 255, 0.95)',
                    titleColor: textColor,
                    bodyColor: textColor,
                    borderColor: gridColor,
                    borderWidth: 1,
                    padding: 12,
                    displayColors: true,
                    callbacks: {
                        label: function(context) {
                            return `Candidates: ${context.parsed.y}`;
                        }
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        stepSize: 1,
                        color: textColor,
                        font: {
                            size: 12,
                            weight: '700'
                        }
                    },
                    grid: {
                        color: gridColor
                    }
                },
                x: {
                    ticks: {
                        color: textColor,  // COSMETIC FIX: Ensures white text in dark mode
                        font: {
                            size: 9.5,
                            weight: '600',
                            lineHeight: 1.3
                        },
                        autoSkip: false,
                        maxRotation: 0,
                        minRotation: 0,
                        padding: 6,
                        align: 'center'  // COSMETIC FIX: Center-align labels for equal spacing
                    },
                    grid: {
                        display: false,
                        offset: false  // COSMETIC FIX: Ensures equal spacing distribution
                    },
                    // COSMETIC FIX: Equal bar width and spacing
                    offset: true,
                    // Ensure bars are centered under labels
                    barPercentage: 0.9,
                    categoryPercentage: 0.85
                }
            }
        }
    });
    
    console.log('Score chart created successfully');
}

function generateSkillsChart(matchResults) {
    console.log('=== SKILLS CHART DEBUG START ===');
    
    const canvasElement = document.getElementById('skills-chart');
    const chartContainer = canvasElement ? (canvasElement.closest('.chart-container') || canvasElement.parentElement) : null;
    
    console.log('1. Canvas element exists:', !!canvasElement);
    console.log('2. Chart container exists:', !!chartContainer);
    
    if (!canvasElement || !chartContainer) {
        console.error('❌ Canvas or container not found!');
        return;
    }
    
    // Destroy existing chart if it exists
    if (skillsChart) {
        try {
            skillsChart.destroy();
            skillsChart = null;
            console.log('3. Existing chart destroyed');
        } catch (e) {
            console.error('Error destroying chart:', e);
        }
    }
    
    // Safety check for data
    if (!matchResults || matchResults.length === 0) {
        console.log('❌ No match results');
        chartContainer.innerHTML = `
            <p style="text-align:center;padding:40px;color:var(--text-secondary);font-size:13px;">
                <i class="fas fa-info-circle" style="display:block;font-size:40px;margin-bottom:12px;opacity:0.5;"></i>
                No skills data available
            </p>
        `;
        return;
    }
    
    // Ensure canvas exists
    if (!document.getElementById('skills-chart')) {
        console.log('4. Recreating canvas');
        chartContainer.innerHTML = '<canvas id="skills-chart"></canvas>';
    }
    
    const ctx = document.getElementById('skills-chart');
    if (!ctx) {
        console.error('❌ Cannot find/create canvas');
        chartContainer.innerHTML = '<p style="text-align:center;padding:40px;color:var(--danger-color);font-size:13px;">Unable to create chart</p>';
        return;
    }
    
    // Calculate skills match from average scores
    const totalScore = matchResults.reduce((sum, r) => {
        const score = r.score || r.match_score || 0;
        return sum + (score <= 10 ? score * 10 : score);
    }, 0);
    
    const avgScore = totalScore / matchResults.length;
    const skillsMatchPercentage = Math.round(avgScore);
    const skillsGapPercentage = 100 - skillsMatchPercentage;
    
    console.log('5. Skills calculation - Match:', skillsMatchPercentage, '% Gap:', skillsGapPercentage, '%');
    
    // Get theme
    const theme = document.documentElement.getAttribute('data-theme') || 'light';
    const isDark = theme === 'dark';
    const textColor = isDark ? '#f1f5f9' : '#0f172a';
    
    console.log('6. Theme:', theme, 'Text color:', textColor);
    
    // Verify Chart.js is loaded
    if (typeof Chart === 'undefined') {
        console.error('❌ Chart.js not loaded');
        chartContainer.innerHTML = '<p style="text-align:center;padding:40px;color:var(--danger-color);font-size:13px;">Chart library not available</p>';
        return;
    }
    
    try {
        skillsChart = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: [
                    `Matching Skills (${skillsMatchPercentage}%)`,
                    `Skills Gap (${skillsGapPercentage}%)`
                ],
                datasets: [{
                    data: [skillsMatchPercentage, skillsGapPercentage],
                    backgroundColor: [
                        'rgba(16, 185, 129, 0.8)',
                        'rgba(239, 68, 68, 0.8)'
                    ],
                    borderColor: [
                        'rgba(16, 185, 129, 1)',
                        'rgba(239, 68, 68, 1)'
                    ],
                    borderWidth: 2,
                    borderRadius: 8,
                    spacing: 2
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                cutout: '65%',
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: {
                            color: textColor,
                            font: {
                                size: 13,
                                weight: '700'
                            },
                            padding: 20,
                            usePointStyle: true,
                            pointStyle: 'circle',
                            boxWidth: 12,
                            boxHeight: 12
                        }
                    },
                    tooltip: {
                        backgroundColor: isDark ? 'rgba(30, 41, 59, 0.95)' : 'rgba(255, 255, 255, 0.95)',
                        titleColor: textColor,
                        bodyColor: textColor,
                        borderColor: isDark ? '#475569' : '#e2e8f0',
                        borderWidth: 1,
                        padding: 12,
                        displayColors: true,
                        callbacks: {
                            label: function(context) {
                                return ` ${context.label}`;
                            }
                        }
                    }
                },
                animation: {
                    animateScale: true,
                    animateRotate: true
                }
            }
        });
        
        console.log('7. ✅ Skills chart created successfully');
        console.log('=== SKILLS CHART DEBUG END ===');
        
    } catch (error) {
        console.error('❌ Error creating chart:', error);
        chartContainer.innerHTML = `
            <p style="text-align:center;padding:40px;color:var(--danger-color);font-size:13px;">
                <i class="fas fa-exclamation-triangle" style="display:block;font-size:40px;margin-bottom:12px;opacity:0.7;"></i>
                Error creating chart
            </p>
        `;
    }
}

function generateTopCandidates(matchResults) {
    const container = document.getElementById('top-candidates-list');
    
    // Sort by score (0-10 scale) and get top 5
    const topCandidates = [...matchResults]
        .sort((a, b) => (b.score || 0) - (a.score || 0))
        .slice(0, 5);
    
    if (topCandidates.length === 0) {
        container.innerHTML = '<p style="color: var(--text-muted); text-align: center;">No candidates yet</p>';
        return;
    }
    
    container.innerHTML = topCandidates.map((candidate, index) => {
        const score = candidate.score || 0;
        const percentage = ((score / 10) * 100).toFixed(0); // Convert 0-10 to percentage
        
        return `
            <div class="top-candidate">
                <div class="candidate-info">
                    <div class="candidate-rank">${['🥇', '🥈', '🥉', '4', '5'][index]}</div>
                    <div class="candidate-name">${candidate.candidate_name || 'Unknown'}</div>
                </div>
                <div class="candidate-score">${percentage}%</div>
            </div>
        `;
    }).join('');
}

function generateQualityMetrics(matchResults) {
    const container = document.getElementById('quality-metrics');
    
    if (!matchResults || matchResults.length === 0) {
        container.innerHTML = '<p style="color: var(--text-secondary); text-align: center; padding: 20px;">No data available</p>';
        return;
    }
    
    // Convert scores to 0-100 scale for consistency
    const scores = matchResults.map(r => {
        const score = r.score || r.match_score || 0;
        return score <= 10 ? score * 10 : score;
    });
    
    // Calculate metrics
    const avgScore = scores.reduce((sum, score) => sum + score, 0) / scores.length;
    const highQuality = scores.filter(score => score >= 70).length;
    const totalCandidates = matchResults.length;
    const qualityRate = totalCandidates > 0 ? (highQuality / totalCandidates * 100).toFixed(0) : 0;
    
    console.log('Quality Metrics:', { avgScore: avgScore.toFixed(1), highQuality, totalCandidates, qualityRate });
    
    const metrics = [
        { icon: 'fa-chart-line', label: 'Average Score', value: `${avgScore.toFixed(1)}%` },
        { icon: 'fa-users', label: 'Total Candidates', value: totalCandidates },
        { icon: 'fa-star', label: 'High Quality (≥70%)', value: highQuality },
        { icon: 'fa-percentage', label: 'Quality Rate', value: `${qualityRate}%` }
    ];
    
    container.innerHTML = metrics.map(metric => `
        <div class="metric-item">
            <div class="metric-label">
                <i class="fas ${metric.icon}"></i>
                ${metric.label}
            </div>
            <div class="metric-value">${metric.value}</div>
        </div>
    `).join('');
}
