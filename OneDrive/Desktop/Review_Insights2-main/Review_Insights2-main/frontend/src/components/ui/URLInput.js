'use client';

import { useState } from 'react';
import styles from './URLInput.module.css';

export default function URLInput({ onSubmit, disabled }) {
  const [url, setUrl] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!url.trim() || disabled) return;

    let finalUrl = url.trim();
    if (!finalUrl.startsWith('http')) {
      finalUrl = 'https://' + finalUrl;
    }
    onSubmit(finalUrl);
  };

  return (
    <div className={styles.container}>
      {/* Brand badge */}
      <div className={styles.badge}>
        <span className={styles.badgeDot} />
        AI-Powered Review Intelligence
      </div>

      <h1 className={styles.title}>
        Understand your products<br />
        through&nbsp;
        <span className={styles.titleGradient}>customer reviews.</span>
      </h1>

      <p className={styles.subtitle}>
        Paste any Amazon or Flipkart product URL and get instant sentiment
        analysis, key themes, and actionable insights — powered by DN Review
        Intelligence System.
      </p>

      <form className={styles.form} onSubmit={handleSubmit}>
        <div className={styles.inputIcon}>
          <svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            <path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71" />
            <path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71" />
          </svg>
        </div>
        <input
          id="url-input"
          type="text"
          className={styles.input}
          placeholder="Paste a product URL (Amazon, Flipkart, etc.)"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          disabled={disabled}
          autoComplete="url"
          required
        />
        <button
          id="analyze-button"
          type="submit"
          className={styles.submitBtn}
          disabled={disabled || !url.trim()}
        >
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
            <circle cx="11" cy="11" r="8" />
            <line x1="21" y1="21" x2="16.65" y2="16.65" />
          </svg>
          Analyze
        </button>
      </form>

      {/* Feature pills */}
      <div className={styles.features}>
        {[
          { icon: '🔍', label: 'Smart Scraping', desc: 'Amazon & Flipkart' },
          { icon: '🧠', label: 'AI Sentiment', desc: 'LLM-powered analysis' },
          { icon: '📊', label: 'Key Themes', desc: 'Auto-extracted topics' },
          { icon: '💡', label: 'Insights', desc: 'Actionable recommendations' },
        ].map(({ icon, label, desc }) => (
          <div key={label} className={styles.featurePill}>
            <span>{icon}</span>
            <div>
              <p className={styles.featureLabel}>{label}</p>
              <p className={styles.featureDesc}>{desc}</p>
            </div>
          </div>
        ))}
      </div>

      {/* Supported platforms */}
      <div className={styles.platforms}>
        <span className={styles.platformLabel}>Supported:</span>
        <span className={styles.platformTag}>Amazon.in</span>
        <span className={styles.platformTag}>Amazon.com</span>
        <span className={styles.platformTag}>Flipkart</span>
      </div>
    </div>
  );
}
