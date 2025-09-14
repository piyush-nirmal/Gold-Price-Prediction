// Custom JavaScript for Smart Gold Investment Advisor

class GoldAdvisorApp {
    constructor() {
        this.currentData = null;
        this.refreshInterval = null;
        this.charts = {};
        this.init();
    }
    
    init() {
        this.setupEventListeners();
        this.loadInitialData();
        this.startAutoRefresh();
    }
    
    setupEventListeners() {
        // File upload form
        const uploadForm = document.getElementById('uploadForm');
        if (uploadForm) {
            uploadForm.addEventListener('submit', (e) => this.handleFileUpload(e));
        }
        
        // Refresh button
        const refreshBtn = document.getElementById('refreshBtn');
        if (refreshBtn) {
            refreshBtn.addEventListener('click', () => this.refreshAllData());
        }
        
        // Chart resize handler
        window.addEventListener('resize', () => this.resizeCharts());
    }
    
    async loadInitialData() {
        try {
            await Promise.all([
                this.loadCurrentPrice(),
                this.loadPredictions(),
                this.loadCharts()
            ]);
        } catch (error) {
            console.error('Error loading initial data:', error);
            this.showNotification('Error loading data. Please refresh the page.', 'error');
        }
    }
    
    async loadCurrentPrice() {
        try {
            const response = await fetch('/api/current_price');
            const data = await response.json();
            
            if (data.status === 'success') {
                this.updateCurrentPrice(data.price, data.timestamp);
            } else {
                throw new Error(data.error || 'Failed to load current price');
            }
        } catch (error) {
            console.error('Error loading current price:', error);
            this.updateCurrentPrice(1800, new Date().toISOString());
        }
    }
    
    updateCurrentPrice(price, timestamp) {
        const priceElement = document.getElementById('currentPrice');
        const timestampElement = document.getElementById('lastUpdated');
        
        if (priceElement) {
            priceElement.textContent = `$${price.toFixed(2)}`;
            priceElement.classList.add('fade-in');
        }
        
        if (timestampElement) {
            timestampElement.textContent = `Last updated: ${new Date(timestamp).toLocaleString()}`;
        }
        
        // Add price change indicator if we have previous data
        if (this.currentData && this.currentData.current_price) {
            const change = ((price - this.currentData.current_price) / this.currentData.current_price) * 100;
            this.updatePriceChange(change);
        }
    }
    
    updatePriceChange(changePercent) {
        const changeElement = document.getElementById('priceChange');
        if (changeElement) {
            const changeClass = changePercent >= 0 ? 'positive' : 'negative';
            const changeSymbol = changePercent >= 0 ? '+' : '';
            changeElement.innerHTML = `
                <span class="${changeClass}">
                    <i class="fas fa-arrow-${changePercent >= 0 ? 'up' : 'down'}"></i>
                    ${changeSymbol}${changePercent.toFixed(2)}%
                </span>
            `;
        }
    }
    
    async loadPredictions() {
        try {
            const response = await fetch('/api/prediction');
            const data = await response.json();
            
            if (data.status === 'success') {
                this.currentData = data;
                this.displayRecommendation(data.recommendation);
                this.displayPredictions(data);
            } else {
                throw new Error(data.error || 'Failed to load predictions');
            }
        } catch (error) {
            console.error('Error loading predictions:', error);
            this.showError('Error loading predictions: ' + error.message);
        }
    }
    
    displayRecommendation(recommendation) {
        const content = document.getElementById('recommendationContent');
        if (!content) return;
        
        const badgeClass = `recommendation-${recommendation.recommendation.toLowerCase()}`;
        const confidenceLevel = this.getConfidenceLevel(recommendation.confidence);
        
        content.innerHTML = `
            <div class="recommendation-badge ${badgeClass} fade-in">
                <i class="fas fa-${this.getRecommendationIcon(recommendation.recommendation)}"></i>
                ${recommendation.recommendation}
            </div>
            <div class="row">
                <div class="col-md-6">
                    <div class="card">
                        <div class="card-body">
                            <h5><i class="fas fa-chart-line"></i> Price Analysis</h5>
                            <p><strong>Current Price:</strong> $${recommendation.current_price.toFixed(2)}</p>
                            <p><strong>Predicted Price:</strong> $${recommendation.predicted_price.toFixed(2)}</p>
                            <p><strong>Expected Change:</strong> 
                                <span class="${recommendation.price_change_pct >= 0 ? 'positive' : 'negative'}">
                                    ${recommendation.price_change_pct >= 0 ? '+' : ''}${recommendation.price_change_pct.toFixed(2)}%
                                </span>
                            </p>
                            <p><strong>Confidence:</strong> 
                                <span class="badge bg-${confidenceLevel.color}">${confidenceLevel.text}</span>
                            </p>
                        </div>
                    </div>
                </div>
                <div class="col-md-6">
                    <div class="card">
                        <div class="card-body">
                            <h5><i class="fas fa-lightbulb"></i> Reasoning</h5>
                            <ul class="reasoning-list">
                                ${recommendation.reasoning.map(reason => `<li class="slide-in-left">${reason}</li>`).join('')}
                            </ul>
                        </div>
                    </div>
                </div>
            </div>
        `;
    }
    
    displayPredictions(data) {
        const content = document.getElementById('predictionsContent');
        if (!content) return;
        
        content.innerHTML = `
            <div class="prediction-item slide-in-left">
                <h5><i class="fas fa-calendar-day"></i> Next Day Prediction</h5>
                <div class="d-flex justify-content-between align-items-center">
                    <span>$${data.next_day_price.toFixed(2)}</span>
                    <span class="badge bg-info">Tomorrow</span>
                </div>
            </div>
            <div class="prediction-item slide-in-right">
                <h5><i class="fas fa-calendar-week"></i> Next Week Predictions</h5>
                <div class="row">
                    ${data.next_week_prices.map((price, index) => `
                        <div class="col-6 col-md-4 mb-2">
                            <div class="d-flex justify-content-between">
                                <small>Day ${index + 1}:</small>
                                <small><strong>$${price.toFixed(2)}</strong></small>
                            </div>
                        </div>
                    `).join('')}
                </div>
            </div>
        `;
    }
    
    async loadCharts() {
        try {
            const response = await fetch('/api/chart_data');
            const data = await response.json();
            
            if (data.status === 'success') {
                this.renderCharts(data);
            } else {
                throw new Error(data.error || 'Failed to load chart data');
            }
        } catch (error) {
            console.error('Error loading charts:', error);
            this.showError('Error loading charts: ' + error.message);
        }
    }
    
    renderCharts(data) {
        try {
            const priceChartData = JSON.parse(data.price_chart);
            const sentimentChartData = JSON.parse(data.sentiment_chart);
            
            // Render price chart
            const priceChartElement = document.getElementById('priceChart');
            if (priceChartElement) {
                Plotly.newPlot('priceChart', priceChartData.data, priceChartData.layout, {
                    responsive: true,
                    displayModeBar: true,
                    modeBarButtonsToRemove: ['pan2d', 'lasso2d', 'select2d']
                });
                this.charts.priceChart = 'priceChart';
            }
            
            // Render sentiment chart
            const sentimentChartElement = document.getElementById('sentimentChart');
            if (sentimentChartElement) {
                Plotly.newPlot('sentimentChart', sentimentChartData.data, sentimentChartData.layout, {
                    responsive: true,
                    displayModeBar: true,
                    modeBarButtonsToRemove: ['pan2d', 'lasso2d', 'select2d']
                });
                this.charts.sentimentChart = 'sentimentChart';
            }
        } catch (error) {
            console.error('Error rendering charts:', error);
        }
    }
    
    async handleFileUpload(event) {
        event.preventDefault();
        
        const formData = new FormData();
        const goldFile = document.getElementById('goldFile').files[0];
        const sentimentFile = document.getElementById('sentimentFile').files[0];
        
        if (!goldFile || !sentimentFile) {
            this.showNotification('Please select both gold price and sentiment files', 'error');
            return;
        }
        
        formData.append('gold_file', goldFile);
        formData.append('sentiment_file', sentimentFile);
        
        const statusDiv = document.getElementById('uploadStatus');
        if (statusDiv) {
            statusDiv.innerHTML = `
                <div class="alert alert-info">
                    <div class="spinner-border spinner-border-sm me-2" role="status"></div>
                    Retraining model with your data...
                </div>
            `;
        }
        
        try {
            const response = await fetch('/upload', {
                method: 'POST',
                body: formData
            });
            
            const result = await response.json();
            
            if (result.status === 'success') {
                this.showNotification('Model retrained successfully! Refreshing data...', 'success');
                setTimeout(() => {
                    this.refreshAllData();
                }, 2000);
            } else {
                this.showNotification('Error: ' + result.message, 'error');
            }
        } catch (error) {
            this.showNotification('Error uploading files: ' + error.message, 'error');
        }
    }
    
    refreshAllData() {
        this.loadInitialData();
        this.showNotification('Data refreshed successfully!', 'success');
    }
    
    startAutoRefresh() {
        // Refresh every 5 minutes
        this.refreshInterval = setInterval(() => {
            this.loadCurrentPrice();
            this.loadPredictions();
        }, 300000);
    }
    
    stopAutoRefresh() {
        if (this.refreshInterval) {
            clearInterval(this.refreshInterval);
            this.refreshInterval = null;
        }
    }
    
    resizeCharts() {
        Object.values(this.charts).forEach(chartId => {
            if (document.getElementById(chartId)) {
                Plotly.Plots.resize(chartId);
            }
        });
    }
    
    getConfidenceLevel(confidence) {
        if (confidence > 0.7) {
            return { text: 'High', color: 'success' };
        } else if (confidence > 0.4) {
            return { text: 'Medium', color: 'warning' };
        } else {
            return { text: 'Low', color: 'danger' };
        }
    }
    
    getRecommendationIcon(recommendation) {
        switch (recommendation.toLowerCase()) {
            case 'buy': return 'arrow-up';
            case 'sell': return 'arrow-down';
            case 'hold': return 'pause';
            default: return 'question';
        }
    }
    
    showNotification(message, type = 'info') {
        const alertClass = `alert-${type}`;
        const notification = document.createElement('div');
        notification.className = `alert ${alertClass} alert-dismissible fade show position-fixed`;
        notification.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
        notification.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        document.body.appendChild(notification);
        
        // Auto remove after 5 seconds
        setTimeout(() => {
            if (notification.parentNode) {
                notification.parentNode.removeChild(notification);
            }
        }, 5000);
    }
    
    showError(message) {
        const content = document.getElementById('recommendationContent');
        if (content) {
            content.innerHTML = `
                <div class="alert alert-danger fade-in">
                    <i class="fas fa-exclamation-triangle"></i> ${message}
                </div>
            `;
        }
    }
}

// Initialize the application when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    window.goldAdvisorApp = new GoldAdvisorApp();
});

// Export for potential use in other scripts
if (typeof module !== 'undefined' && module.exports) {
    module.exports = GoldAdvisorApp;
}
