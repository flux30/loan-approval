/**
 * Loan Approval System - Frontend Logic
 */

const API_BASE = 'http://localhost:5000/api';

gsap.registerPlugin(ScrollTrigger);

document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

function initializeApp() {
    initializeEventListeners();
    loadApplicants();
}

function initializeEventListeners() {
    document.getElementById('evalAllBtn')?.addEventListener('click', evaluateAll);
    document.getElementById('customEvalBtn')?.addEventListener('click', openModal);
    document.getElementById('modalCloseBtn')?.addEventListener('click', closeModal);
    document.getElementById('traceCloseBtn')?.addEventListener('click', closeTraceModal);
    document.getElementById('customEvalForm')?.addEventListener('submit', handleFormSubmit);
    document.getElementById('formCancelBtn')?.addEventListener('click', closeModal);
    
    document.getElementById('customEvalModal')?.addEventListener('click', function(e) {
        if (e.target === this) closeModal();
    });
    
    document.getElementById('traceModal')?.addEventListener('click', function(e) {
        if (e.target === this) closeTraceModal();
    });
}

async function loadApplicants() {
    try {
        const response = await fetch(`${API_BASE}/applicants`);
        const data = await response.json();
        
        if (data.success) {
            populateTable(data.data);
        }
    } catch (error) {
        console.error('Error:', error);
    }
}

function populateTable(applicants) {
    const tbody = document.getElementById('applicantsTableBody');
    if (!tbody) return;
    
    tbody.innerHTML = '';
    applicants.forEach(app => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${app.applicant_id}</td>
            <td>$${app.income.toLocaleString()}</td>
            <td>${app.credit_score}</td>
            <td>${app.employment_status}</td>
            <td>${app.employment_duration}</td>
            <td>${app.age}</td>
            <td>${app.dependents}</td>
            <td>${app.existing_debt}</td>
            <td><span class="status-badge status-review" data-id="${app.applicant_id}">Pending</span></td>
        `;
        tbody.appendChild(row);
        
        gsap.from(row, {
            opacity: 0,
            y: 10,
            duration: 0.4
        });
    });
}

async function evaluateAll() {
    const btn = document.getElementById('evalAllBtn');
    btn.disabled = true;
    btn.textContent = 'Evaluating...';
    
    try {
        const response = await fetch(`${API_BASE}/evaluate-all`);
        const data = await response.json();
        
        if (data.success) {
            updateTableStatuses(data.data);
            displayResults(data.data, data.statistics);
            showNotification('Evaluation complete!', 'success');
        } else {
            showNotification(data.error || 'Evaluation failed', 'error');
        }
    } catch (error) {
        console.error('Error:', error);
        showNotification('Error evaluating applicants', 'error');
    } finally {
        btn.disabled = false;
        btn.textContent = 'Evaluate All Applicants';
    }
}

function updateTableStatuses(results) {
    results.forEach(result => {
        const badge = document.querySelector(`span[data-id="${result.applicant_id}"]`);
        if (badge) {
            const decision = result.final_decision;
            const statusClass = getStatusClass(decision);
            badge.textContent = decision;
            badge.className = `status-badge ${statusClass}`;
        }
    });
}

function displayResults(results, stats) {
    const section = document.getElementById('resultsSection');
    const container = document.getElementById('resultsCardsContainer');
    
    section.classList.add('active');
    
    updateStatsAnimated(stats);
    
    container.innerHTML = '';
    results.forEach((result, i) => {
        const card = createResultCard(result);
        container.appendChild(card);
        
        gsap.from(card, {
            opacity: 0,
            y: 20,
            duration: 0.4,
            delay: i * 0.05
        });
    });
    
    setTimeout(() => {
        section.scrollIntoView({ behavior: 'smooth' });
    }, 100);
}

function updateStatsAnimated(stats) {
    const decisions = stats.decisions || {};
    
    animateCounter('totalEvaluated', stats.total_applicants);
    animateCounter('approvedCount', decisions['Approve Loan'] || 0);
    animateCounter('conditionalCount', decisions['Approve with Conditions'] || 0);
    animateCounter('rejectedCount', decisions['Reject Loan'] || 0);
    animateCounter('reviewCount', decisions['Manual Review'] || 0);
}

function animateCounter(id, target) {
    const element = document.getElementById(id);
    gsap.to({ value: 0 }, {
        value: target,
        duration: 1,
        ease: 'power2.out',
        onUpdate: function() {
            element.textContent = Math.round(this.targets()[0].value);
        }
    });
}

function createResultCard(result) {
    const decision = result.final_decision;
    const data = result.applicant_data;
    const statusClass = getStatusClass(decision);
    
    const card = document.createElement('div');
    card.className = `result-card ${statusClass.replace('status-', '')}`;
    
    // Encode result as base64 to avoid quote issues
    const resultStr = btoa(JSON.stringify(result));
    
    card.innerHTML = `
        <div class="result-header">
            <div class="result-id">${result.applicant_id}</div>
            <span class="status-badge ${statusClass}">${decision}</span>
        </div>
        <div class="result-stats">
            <div class="result-stat-item"><strong>Income:</strong> $${data.income.toLocaleString()}</div>
            <div class="result-stat-item"><strong>Credit:</strong> ${data.credit_score}</div>
            <div class="result-stat-item"><strong>Age:</strong> ${data.age}</div>
            <div class="result-stat-item"><strong>Debt:</strong> ${data.existing_debt}</div>
        </div>
        <button class="trace-button" onclick="showTrace('${resultStr}')">
            View Reasoning Trace
        </button>
    `;
    return card;
}

function getStatusClass(decision) {
    const map = {
        'Approve Loan': 'status-approved',
        'Approve with Conditions': 'status-conditional',
        'Reject Loan': 'status-rejected',
        'Manual Review': 'status-review'
    };
    return map[decision] || 'status-review';
}

function showTrace(resultStr) {
    try {
        const result = JSON.parse(atob(resultStr));
        const modal = document.getElementById('traceModal');
        const container = document.getElementById('traceContainer');
        
        container.innerHTML = '';
        
        let trace = [];
        if (result.forward_chaining?.trace?.trace) {
            trace = result.forward_chaining.trace.trace;
        }
        
        if (trace.length === 0) {
            container.innerHTML = '<p style="color: var(--text-secondary); padding: var(--spacing-md);">No trace available</p>';
        } else {
            trace.forEach((entry, i) => {
                const div = document.createElement('div');
                div.className = `trace-entry ${entry.level.toLowerCase()}`;
                div.innerHTML = `
                    <span class="trace-level">${entry.level}</span>
                    <span>${entry.message}${entry.rule_id ? ` [${entry.rule_id}]` : ''}</span>
                `;
                container.appendChild(div);
                
                gsap.from(div, {
                    opacity: 0,
                    x: -10,
                    duration: 0.3,
                    delay: i * 0.02
                });
            });
        }
        
        modal.classList.add('active');
    } catch (error) {
        console.error('Error showing trace:', error);
        showNotification('Error displaying trace', 'error');
    }
}

function openModal() {
    document.getElementById('customEvalModal').classList.add('active');
}

function closeModal() {
    document.getElementById('customEvalModal').classList.remove('active');
    document.getElementById('customEvalForm').reset();
}

function closeTraceModal() {
    document.getElementById('traceModal').classList.remove('active');
}

async function handleFormSubmit(e) {
    e.preventDefault();
    
    const formData = {
        applicant_id: document.getElementById('applicantId').value,
        income: parseInt(document.getElementById('income').value),
        credit_score: parseInt(document.getElementById('creditScore').value),
        employment_status: document.getElementById('employmentStatus').value,
        employment_duration: parseFloat(document.getElementById('employmentDuration').value),
        age: parseInt(document.getElementById('age').value),
        dependents: parseInt(document.getElementById('dependents').value),
        existing_debt: document.getElementById('existingDebt').value
    };
    
    try {
        const response = await fetch(`${API_BASE}/evaluate`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(formData)
        });
        
        const data = await response.json();
        
        if (data.success) {
            closeModal();
            displaySingleResult(data.data);
            showNotification('Evaluation complete!', 'success');
        } else {
            showNotification(data.error || 'Evaluation failed', 'error');
        }
    } catch (error) {
        console.error('Error:', error);
        showNotification('Error evaluating applicant', 'error');
    }
}

function displaySingleResult(result) {
    const section = document.getElementById('resultsSection');
    const container = document.getElementById('resultsCardsContainer');
    
    section.classList.add('active');
    const card = createResultCard(result);
    container.insertBefore(card, container.firstChild);
    
    gsap.from(card, {
        opacity: 0,
        scale: 0.95,
        duration: 0.4
    });
    
    section.scrollIntoView({ behavior: 'smooth' });
}

function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    const colors = {
        success: '#10b981',
        error: '#ef4444',
        info: '#e0e0e0'
    };
    
    notification.style.cssText = `
        position: fixed;
        top: 24px;
        right: 24px;
        padding: 12px 24px;
        background: ${colors[type]};
        color: ${type === 'info' ? '#000000' : '#ffffff'};
        border-radius: 6px;
        font-weight: 600;
        z-index: 2000;
        font-family: 'Lexend', sans-serif;
    `;
    notification.textContent = message;
    document.body.appendChild(notification);
    
    gsap.from(notification, {
        opacity: 0,
        y: -20,
        duration: 0.3
    });
    
    gsap.to(notification, {
        opacity: 0,
        y: -20,
        duration: 0.3,
        delay: 3,
        onComplete: () => notification.remove()
    });
}
