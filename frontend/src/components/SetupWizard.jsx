import React, { useState } from 'react';
import { CheckCircle, BrainCircuit, AlertCircle, ExternalLink } from 'lucide-react';

const SetupWizard = ({ onComplete }) => {
  const [step, setStep] = useState(1);
  const [githubToken, setGithubToken] = useState('');
  const [validating, setValidating] = useState(false);
  const [error, setError] = useState('');

  const validateAndSaveToken = async () => {
    setValidating(true);
    setError('');

    try {
      const response = await fetch('https://api.github.com/user', {
        headers: { 'Authorization': `token ${githubToken}` }
      });

      if (!response.ok) {
        throw new Error('Invalid token. Please check and try again.');
      }

      const userData = await response.json();
      const scopes = response.headers.get('X-OAuth-Scopes');

      if (!scopes || (!scopes.includes('repo') && !scopes.includes('public_repo'))) {
        throw new Error('Token is missing required permissions. Please ensure it has "repo" or "public_repo" scope.');
      }

      const saveResponse = await fetch('/api/config/save-token', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          token: githubToken,
          username: userData.login
        })
      });

      if (!saveResponse.ok) {
        throw new Error('Failed to save token to configuration.');
      }

      setStep(4); // Success step
    } catch (err) {
      setError(err.message);
    } finally {
      setValidating(false);
    }
  };

  return (
    <div className="min-h-screen bg-background-dark flex items-center justify-center p-4 font-sans">
      <div className="max-w-3xl w-full card p-0 overflow-hidden">
        {/* Progress Bar */}
        <div className="bg-panel-dark h-1">
          <div
            className="bg-primary-default h-full transition-all duration-500"
            style={{ width: `${(step / 4) * 100}%` }}
          />
        </div>

        <div className="p-8 sm:p-12">
          {/* Step 1: Welcome */}
          {step === 1 && (
            <div className="text-center">
              <div className="w-20 h-20 bg-panel-dark border-2 border-border-dark rounded-full mx-auto mb-6 flex items-center justify-center">
                <BrainCircuit className="w-10 h-10 text-icon-purple" />
              </div>
              <h1 className="text-h3 mb-4 text-text-dark">
                Welcome to AI Predictions!
              </h1>
              <p className="text-body-large text-light-grey mb-8 max-w-2xl mx-auto">
                In just a few steps, you'll be ready to build and submit machine learning models.
              </p>
              <button
                onClick={() => setStep(2)}
                className="btn-primary px-8 py-3 text-body-medium"
              >
                Get Started
              </button>
            </div>
          )}

          {/* Step 2: GitHub Token Instructions */}
          {step === 2 && (
            <div>
              <h2 className="text-h5 mb-6 text-text-dark">Create Your AIP Access Token</h2>
              <p className="text-body-medium text-light-grey mb-8">
                To submit models, you'll need an AIP Access Token. Follow these steps:
              </p>

              <div className="space-y-4 mb-8">
                <div className="flex gap-4 p-4 bg-panel-dark border border-border-dark rounded-lg">
                  <div className="flex-shrink-0 w-8 h-8 bg-border-dark text-text-dark rounded-full flex items-center justify-center font-bold text-body-small">
                    1
                  </div>
                  <div className="flex-1">
                    <p className="font-bold mb-1 text-text-dark">Go to Token Settings</p>
                    <a
                      href="https://github.com/settings/tokens/new"
                      target="_blank"
                      rel="noopener noreferrer"
                      className="inline-flex items-center gap-2 text-primary-default hover:text-primary-hover font-medium transition-colors"
                    >
                      Open Token Creation Page
                      <ExternalLink className="w-4 h-4" />
                    </a>
                  </div>
                </div>

                <div className="flex gap-4 p-4 bg-panel-dark border border-border-dark rounded-lg">
                  <div className="flex-shrink-0 w-8 h-8 bg-border-dark text-text-dark rounded-full flex items-center justify-center font-bold text-body-small">
                    2
                  </div>
                  <div className="flex-1">
                    <p className="font-bold mb-2 text-text-dark">Configure Your Token</p>
                    <ul className="list-disc list-inside text-light-grey space-y-1 text-body-small">
                      <li><span className="font-medium text-text-dark">Note:</span> "AIP Access"</li>
                      <li><span className="font-medium text-text-dark">Expiration:</span> 90 days (recommended)</li>
                      <li><span className="font-medium text-text-dark">Scopes:</span> Select <code className="bg-border-dark text-light-grey px-2 py-0.5 rounded">repo</code> or <code className="bg-border-dark text-light-grey px-2 py-0.5 rounded">public_repo</code></li>
                    </ul>
                  </div>
                </div>

                <div className="flex gap-4 p-4 bg-panel-dark border border-border-dark rounded-lg">
                  <div className="flex-shrink-0 w-8 h-8 bg-border-dark text-text-dark rounded-full flex items-center justify-center font-bold text-body-small">
                    3
                  </div>
                  <div className="flex-1">
                    <p className="font-bold mb-1 text-text-dark">Generate and Copy Token</p>
                    <p className="text-light-grey text-body-small">Click "Generate token" and copy the new token.</p>
                  </div>
                </div>
              </div>

              <div className="flex gap-4">
                <button
                  onClick={() => setStep(1)}
                  className="btn-secondary px-6 py-3 text-body-medium"
                >
                  Back
                </button>
                <button
                  onClick={() => setStep(3)}
                  className="flex-1 btn-primary px-6 py-3 text-body-medium"
                >
                  I've Created My Token
                </button>
              </div>
            </div>
          )}

          {/* Step 3: Enter Token */}
          {step === 3 && (
            <div>
              <h2 className="text-h5 mb-6 text-text-dark">Enter Your AIP Access Token</h2>
              <p className="text-body-medium text-light-grey mb-8">
                Paste your token below. We'll validate it and save it securely.
              </p>

              <div className="mb-6">
                <label className="block text-body-small font-bold text-text-dark mb-2">
                  AIP Access Token
                </label>
                <input
                  type="password"
                  value={githubToken}
                  onChange={(e) => setGithubToken(e.target.value)}
                  placeholder="ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
                  className="input-field font-mono"
                />
                <p className="text-body-xsmall text-light-grey mt-2">
                  Your token should start with "ghp_".
                </p>
              </div>

              {error && (
                <div className="mb-6 p-4 bg-error/10 border border-error/20 rounded-lg flex items-start gap-3">
                  <AlertCircle className="w-5 h-5 text-error flex-shrink-0 mt-0.5" />
                  <p className="text-error text-body-small">{error}</p>
                </div>
              )}

              <div className="flex gap-4">
                <button
                  onClick={() => setStep(2)}
                  className="btn-secondary px-6 py-3 text-body-medium"
                  disabled={validating}
                >
                  Back
                </button>
                <button
                  onClick={validateAndSaveToken}
                  disabled={!githubToken || validating}
                  className="flex-1 btn-primary px-6 py-3 text-body-medium disabled:opacity-50"
                >
                  {validating ? 'Validating...' : 'Validate & Save Token'}
                </button>
              </div>
            </div>
          )}

          {/* Step 4: Success */}
          {step === 4 && (
            <div className="text-center">
              <div className="w-20 h-20 bg-success/10 border-2 border-success/20 rounded-full mx-auto mb-6 flex items-center justify-center">
                <CheckCircle className="w-12 h-12 text-success" />
              </div>
              <h2 className="text-h3 mb-4 text-text-dark">You're All Set!</h2>
              <p className="text-body-large text-light-grey mb-8 max-w-2xl mx-auto">
                Your token has been saved. You're ready to start building and submitting models.
              </p>
              <div className="bg-panel-dark border border-border-dark rounded-lg p-6 mb-8 text-left">
                <h3 className="text-h7 font-bold mb-4 text-text-dark">Next Steps:</h3>
                <ul className="space-y-3 text-light-grey">
                  <li className="flex items-start gap-3">
                    <CheckCircle className="w-5 h-5 text-success flex-shrink-0 mt-1" />
                    <span>Click "Start Building" to launch the main workspace.</span>
                  </li>
                  <li className="flex items-start gap-3">
                    <CheckCircle className="w-5 h-5 text-success flex-shrink-0 mt-1" />
                    <span>Open a notebook and start building your model.</span>
                  </li>
                  <li className="flex items-start gap-3">
                    <CheckCircle className="w-5 h-5 text-success flex-shrink-0 mt-1" />
                    <span>Use the submission panel to submit your work.</span>
                  </li>
                </ul>
              </div>
              <button
                onClick={onComplete}
                className="btn-primary px-8 py-3 text-body-medium"
              >
                Start Building Models!
              </button>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default SetupWizard;