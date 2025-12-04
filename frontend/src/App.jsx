import { useState, useEffect } from 'react'
import axios from 'axios'
import { Play, Square, Upload, ExternalLink, BrainCircuit, Terminal, Clock } from 'lucide-react'
import SetupWizard from './components/SetupWizard'
import ModelSelectionModal from './components/ModelSelectionModal'
import LoadingOverlay from './components/LoadingOverlay'



function App() {
    const [status, setStatus] = useState('stopped')
    const [jupyterUrl, setJupyterUrl] = useState(null)
    const [loading, setLoading] = useState(false)
    const [message, setMessage] = useState('')
    const [commitMsg, setCommitMsg] = useState('')
    const [description, setDescription] = useState('')
    const [setupComplete, setSetupComplete] = useState(null)
    const [checkingSetup, setCheckingSetup] = useState(true)
    const [history, setHistory] = useState([])
    const [loadingSteps, setLoadingSteps] = useState([])
    const [isModalOpen, setIsModalOpen] = useState(false)
    const [updateAvailable, setUpdateAvailable] = useState(false)
    const [updateInfo, setUpdateInfo] = useState(null)
    const [currentVersion, setCurrentVersion] = useState('...')

    useEffect(() => {
        checkSetupStatus()
    }, [])

    useEffect(() => {
        if (setupComplete) {
            fetchCurrentVersion()
            checkStatus()
            fetchHistory()
            checkUpdates()
            const interval = setInterval(checkStatus, 5000)
            return () => clearInterval(interval)
        }
    }, [setupComplete])

    const checkSetupStatus = async () => {
        try {
            const res = await axios.get('/api/config/check-setup')
            setSetupComplete(res.data.setup_complete)
        } catch (err) {
            console.error("Failed to check setup status", err)
            setSetupComplete(false)
        } finally {
            setCheckingSetup(false)
        }
    }

    const handleSetupComplete = () => {
        setSetupComplete(true)
        window.location.reload()
    }

    const fetchHistory = async () => {
        try {
            const res = await axios.get('/api/history/submissions')
            setHistory(res.data)
        } catch (err) {
            console.error("Failed to fetch history", err)
        }
    }

    const checkStatus = async () => {
        try {
            const res = await axios.get('/api/environment/status')
            setStatus(res.data.status)
            if (res.data.url) setJupyterUrl(res.data.url)
        } catch (err) {
            console.error("Failed to check status", err)
        }
    }

    const fetchCurrentVersion = async () => {
        try {
            const res = await axios.get('/api/updates/current-version')
            setCurrentVersion(res.data.version)
        } catch (err) {
            console.error("Failed to fetch version", err)
            setCurrentVersion('1.0.0')
        }
    }

    const checkUpdates = async () => {
        try {
            const res = await axios.get('/api/updates/check')
            if (res.data.update_available) {
                setUpdateAvailable(true)
                setUpdateInfo(res.data)
            }
        } catch (err) {
            console.error("Failed to check for updates", err)
        }
    }

    const performUpdate = async () => {
        if (!window.confirm("This will stop the application and install the latest version. Continue?")) return

        setLoading(true)
        setMessage('Installing update...')

        // Initialize update steps
        const steps = [
            { label: 'Validating prerequisites...', status: 'processing' },
            { label: 'Creating backup...', status: 'pending' },
            { label: 'Downloading update...', status: 'pending' },
            { label: 'Applying changes...', status: 'pending' },
            { label: 'Restarting application...', status: 'pending' }
        ]
        setLoadingSteps(steps)

        try {
            // Start the update
            await axios.post('/api/updates/perform')

            // Simulate step progression while polling for status
            let currentStep = 0
            let pollCount = 0
            const maxPolls = 60 // 2 minutes max

            const pollInterval = setInterval(async () => {
                pollCount++

                try {
                    const status = await axios.get('/api/updates/status')

                    // Update steps based on status message
                    if (status.data.message.includes('backup')) {
                        currentStep = Math.max(currentStep, 1)
                    } else if (status.data.message.includes('download') || status.data.message.includes('Fetching')) {
                        currentStep = Math.max(currentStep, 2)
                    } else if (status.data.message.includes('Applying') || status.data.message.includes('update')) {
                        currentStep = Math.max(currentStep, 3)
                    } else if (status.data.message.includes('restart')) {
                        currentStep = Math.max(currentStep, 4)
                    }

                    // Update step statuses
                    setLoadingSteps(prev => prev.map((step, idx) => ({
                        ...step,
                        status: idx < currentStep ? 'completed' : idx === currentStep ? 'processing' : 'pending'
                    })))

                    if (status.data.complete || status.data.error) {
                        clearInterval(pollInterval)

                        if (status.data.error) {
                            setMessage(`Update failed: ${status.data.error}`)
                            setLoading(false)
                            setLoadingSteps([])
                        } else {
                            // Mark all as completed
                            setLoadingSteps(prev => prev.map(step => ({ ...step, status: 'completed' })))
                            setMessage('Update complete! Reloading...')
                            setTimeout(() => window.location.reload(), 2000)
                        }
                    }
                } catch (err) {
                    // Backend might be down during restart, this is expected
                    // Move to restart step
                    currentStep = Math.max(currentStep, 4)
                    setLoadingSteps(prev => prev.map((step, idx) => ({
                        ...step,
                        status: idx < currentStep ? 'completed' : idx === currentStep ? 'processing' : 'pending'
                    })))
                }

                // Timeout after max polls
                if (pollCount >= maxPolls) {
                    clearInterval(pollInterval)
                    setMessage('Update taking longer than expected. Please reload manually.')
                    setTimeout(() => {
                        setLoading(false)
                        setLoadingSteps([])
                    }, 5000)
                }
            }, 2000)

        } catch (err) {
            setMessage("Update failed: " + (err.response?.data?.detail || err.message))
            setLoading(false)
            setLoadingSteps([])
        }
    }

    // Helper function to ensure all loading steps complete smoothly
    const completeAllSteps = async (steps) => {
        return new Promise((resolve) => {
            const totalSteps = steps.length
            let currentStep = 0

            const interval = setInterval(() => {
                currentStep++
                if (currentStep < totalSteps) {
                    setLoadingSteps(prev => prev.map((step, idx) => ({
                        ...step,
                        status: idx < currentStep ? 'completed' : idx === currentStep ? 'processing' : 'pending'
                    })))
                } else {
                    // Mark all as completed
                    setLoadingSteps(prev => prev.map(step => ({ ...step, status: 'completed' })))
                    clearInterval(interval)
                    setTimeout(resolve, 500) // Brief pause to show all completed
                }
            }, 600)
        })
    }

    const startEnv = async (modelId) => {
        console.log('startEnv called with modelId:', modelId)
        setIsModalOpen(false)
        setLoading(true)
        setMessage('Starting environment...')

        // Initialize steps
        const steps = [
            { label: 'Validating configuration...', status: 'processing' },
            { label: 'Allocating resources...', status: 'pending' },
            { label: 'Starting Jupyter kernel...', status: 'pending' },
            { label: 'Connecting to workspace...', status: 'pending' }
        ]
        setLoadingSteps(steps)

        try {
            console.log('Making API request to /api/environment/start')

            // Start the API call and step progression in parallel
            const [apiResult] = await Promise.all([
                axios.post('/api/environment/start', {
                    template_id: 'default',
                    model_id: modelId
                }),
                completeAllSteps(steps)
            ])

            console.log('API response:', apiResult.data)
            setStatus('running')
            setJupyterUrl(apiResult.data.url)
            setMessage('Environment started!')
        } catch (err) {
            console.error('Error starting environment:', err)
            const detail = err.response?.data?.detail || err.message;
            setMessage('Error starting environment: ' + detail);
        } finally {
            setLoading(false)
            setLoadingSteps([])
        }
    }

    const stopEnv = async () => {
        setLoading(true)
        setMessage('Stopping environment...')

        const steps = [
            { label: 'Stopping Jupyter kernel...', status: 'processing' },
            { label: 'Saving workspace state...', status: 'pending' },
            { label: 'Releasing resources...', status: 'pending' },
            { label: 'Disconnecting...', status: 'pending' }
        ]
        setLoadingSteps(steps)

        try {
            // Start the API call and step progression in parallel
            await Promise.all([
                axios.post('/api/environment/stop'),
                completeAllSteps(steps)
            ])

            setStatus('stopped')
            setJupyterUrl(null)
            setMessage('Environment stopped.')
        } catch (err) {
            setMessage('Error stopping environment: ' + err.message)
        } finally {
            setLoading(false)
            setLoadingSteps([])
        }
    }

    const restoreSubmission = async (item) => {
        if (!window.confirm(`Are you sure you want to restore "${item.title}"? This will overwrite your current workspace.`)) {
            return
        }

        setLoading(true)
        setMessage(`Restoring workspace from "${item.title}"...`)
        try {
            const res = await axios.post('/api/history/restore', {
                sha: item.sha,
                branch: item.branch
            })
            setMessage(`Success! Workspace restored. Backup saved at: ${res.data.backup_path}`)
        } catch (err) {
            setMessage('Restore failed: ' + (err.response?.data?.detail || err.message))
        } finally {
            setLoading(false)
        }
    }

    const submitModel = async (e) => {
        e.preventDefault()
        setLoading(true)
        setMessage('Submitting model to AIP...')

        // Initialize submission steps
        const steps = [
            { label: 'Preparing workspace...', status: 'processing' },
            { label: 'Creating Git commit...', status: 'pending' },
            { label: 'Pushing to GitHub...', status: 'pending' },
            { label: 'Creating pull request...', status: 'pending' }
        ]
        setLoadingSteps(steps)

        try {
            // Start the API call and step progression in parallel
            const [apiResult] = await Promise.all([
                axios.post('/api/submission/submit', {
                    commit_message: commitMsg,
                    description: description
                }),
                completeAllSteps(steps)
            ])

            setMessage('Success! Your model has been submitted to AIP.')
            setCommitMsg('')
            setDescription('')
            fetchHistory()
        } catch (err) {
            setMessage('Submission failed: ' + (err.response?.data?.detail || err.message))
        } finally {
            setLoading(false)
            setLoadingSteps([])
        }
    }

    if (checkingSetup) {
        const steps = [
            { label: 'Connecting to backend...', status: 'completed' },
            { label: 'Checking configuration...', status: 'processing' },
            { label: 'Verifying setup status...', status: 'pending' }
        ]
        return <LoadingOverlay message="Initializing application..." steps={steps} />
    }

    if (!setupComplete) {
        return <SetupWizard onComplete={handleSetupComplete} />
    }

    const Snowflakes = () => {
        return (
            <>
                {[...Array(20)].map((_, i) => (
                    <div
                        key={i}
                        className="snowflake"
                        style={{
                            left: `${Math.random() * 100}%`,
                            animationDuration: `${5 + Math.random() * 10}s`,
                            animationDelay: `${Math.random() * 5}s`,
                            fontSize: `${0.5 + Math.random() * 1}em`,
                        }}
                    >
                        ❄
                    </div>
                ))}
            </>
        );
    };

    return (
        <div className="min-h-screen bg-gradient-to-br from-red-950 via-red-900 to-red-950 text-text-dark p-8 font-sans">
            <Snowflakes />
            <div className="max-w-6xl mx-auto">
                <div className="text-center mb-6">
                    <h2 className="text-3xl font-bold text-white drop-shadow-lg">
                        🎄 Happy Holidays! 🎅
                    </h2>
                    <p className="text-red-100 mt-2">Christmas Edition</p>
                </div>
                <header className="mb-12 border-b border-border-dark pb-6 flex items-center justify-between">
                    <div>
                        <h1 className="text-h4 tracking-[-1px] font-bold text-text-dark">
                            AI Predictions
                        </h1>
                        <p className="text-body-large text-light-grey mt-1">Model Builder Workspace</p>
                    </div>
                    <div className="px-4 py-2 rounded-md bg-panel-dark border border-border-dark text-light-grey text-body-small font-mono">
                        v{currentVersion}
                    </div>
                </header>

                {updateAvailable && (
                    <div className="mb-8 p-4 bg-primary-default/10 border border-primary-default rounded-lg flex items-center justify-between">
                        <div className="flex items-center gap-3">
                            <div className="p-2 bg-primary-default rounded-full text-background-dark">
                                <Upload size={20} />
                            </div>
                            <div className="flex-1">
                                <h3 className="font-bold text-body-medium">Update Available: v{updateInfo?.latest_version}</h3>
                                <p className="text-body-small text-light-grey">A new version of AIP Notebook is available.</p>
                            </div>
                        </div>
                        <button
                            onClick={performUpdate}
                            disabled={loading}
                            className="btn-primary disabled:opacity-50 disabled:cursor-not-allowed">
                            {loading ? 'Updating...' : 'Update Now'}
                        </button>
                    </div>
                )}

                <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                    {/* Environment Control */}
                    <div className="card p-8">
                        <div className="flex items-center justify-between mb-8">
                            <h2 className="text-h6 flex items-center gap-3 font-semibold">
                                <Terminal className="text-icon-blue" />
                                Dev Environment
                            </h2>
                            <span className={`px-3 py-1 rounded-full text-body-xsmall font-bold ${status === 'running'
                                ? 'bg-success/10 text-success'
                                : 'bg-error/10 text-error'
                                }`}>
                                {status.toUpperCase()}
                            </span>
                        </div>

                        <div className="space-y-6">
                            {status === 'stopped' ? (
                                <button
                                    onClick={() => setIsModalOpen(true)}
                                    disabled={loading}
                                    className="btn-primary w-full py-3 text-body-medium disabled:opacity-50"
                                >
                                    <Play size={20} /> Start Environment
                                </button>
                            ) : (
                                <div className="space-y-4">
                                    <a
                                        href={jupyterUrl}
                                        target="_blank"
                                        rel="noreferrer"
                                        className="block w-full text-center py-3 bg-success hover:bg-success/80 text-text-dark rounded-lg font-semibold text-body-medium flex items-center justify-center gap-3 transition-colors"
                                    >
                                        <ExternalLink size={20} /> Open Jupyter Notebook
                                    </a>
                                    <button
                                        onClick={stopEnv}
                                        disabled={loading}
                                        className="w-full py-3 bg-error/10 hover:bg-error/20 text-error rounded-lg font-medium flex items-center justify-center gap-3 transition-colors disabled:opacity-50"
                                    >
                                        <Square size={20} /> Stop Environment
                                    </button>
                                </div>
                            )}
                            <p className="text-body-small text-light-grey text-center">
                                {status === 'stopped'
                                    ? 'Start the environment to begin coding your models.'
                                    : 'Your environment is active and ready for development.'}
                            </p>
                        </div>
                    </div>

                    {/* Submission Control */}
                    <div className="card p-8">
                        <h2 className="text-h6 flex items-center gap-3 mb-8 font-semibold">
                            <BrainCircuit className="text-icon-purple" />
                            Submit Model
                        </h2>

                        <form onSubmit={submitModel} className="space-y-6">
                            <div>
                                <label className="block text-body-small font-bold text-light-grey mb-2">Commit Message</label>
                                <input
                                    type="text"
                                    value={commitMsg}
                                    onChange={(e) => setCommitMsg(e.target.value)}
                                    className="input-field"
                                    placeholder="e.g. Added linear regression model"
                                    required
                                />
                            </div>
                            <div>
                                <label className="block text-body-small font-bold text-light-grey mb-2">Description</label>
                                <textarea
                                    value={description}
                                    onChange={(e) => setDescription(e.target.value)}
                                    className="input-field h-32 resize-none"
                                    placeholder="Describe your changes and model performance..."
                                    required
                                />
                            </div>
                            <button
                                type="submit"
                                disabled={loading || status !== 'running'}
                                className="btn-primary w-full py-3 text-body-medium flex items-center justify-center gap-3 disabled:opacity-50"
                            >
                                <Upload size={20} /> Submit to AIP
                            </button>
                        </form>
                    </div>
                </div>

                {/* Status Message */}
                {message && (
                    <div className="mt-8 p-4 card border-l-4 border-info text-center text-info">
                        {message}
                    </div>
                )}

                {/* History Section */}
                <div className="mt-12 card p-8">
                    <div className="flex items-center justify-between mb-8">
                        <h2 className="text-h6 flex items-center gap-3 font-semibold">
                            <Clock className="text-icon-green" />
                            Submission History
                        </h2>
                        <button
                            onClick={fetchHistory}
                            className="btn-secondary text-body-small"
                        >
                            Refresh List
                        </button>
                    </div>

                    <div className="overflow-x-auto">
                        <table className="w-full text-left">
                            <thead>
                                <tr className="border-b border-border-dark">
                                    <th className="px-6 py-4 text-body-small font-bold text-light-grey uppercase tracking-wider">Title</th>
                                    <th className="px-6 py-4 text-body-small font-bold text-light-grey uppercase tracking-wider">Date</th>
                                    <th className="px-6 py-4 text-body-small font-bold text-light-grey uppercase tracking-wider">Status</th>
                                    <th className="px-6 py-4 text-body-small font-bold text-light-grey uppercase tracking-wider text-right">Action</th>
                                </tr>
                            </thead>
                            <tbody className="divide-y divide-border-dark">
                                {history.length === 0 ? (
                                    <tr>
                                        <td colSpan="4" className="px-6 py-12 text-center text-light-grey">
                                            <div className="flex flex-col items-center gap-3">
                                                <BrainCircuit className="w-12 h-12 opacity-20" />
                                                <p>No submissions found yet.</p>
                                            </div>
                                        </td>
                                    </tr>
                                ) : (
                                    history.map((item) => (
                                        <tr key={item.id} className="hover:bg-panel-dark/50 transition-colors">
                                            <td className="px-6 py-4 text-body-medium text-text-dark">
                                                {item.title}
                                            </td>
                                            <td className="px-6 py-4 text-body-small text-light-grey">
                                                {new Date(item.created_at).toLocaleString()}
                                            </td>
                                            <td className="px-6 py-4">
                                                <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-body-xsmall font-medium ${item.state === 'open'
                                                    ? 'bg-success/10 text-success'
                                                    : 'bg-icon-purple/10 text-icon-purple'
                                                    }`}>
                                                    {item.state === 'open' ? 'Submitted' : 'Processed'}
                                                </span>
                                            </td>
                                            <td className="px-6 py-4 text-right">
                                                <button
                                                    onClick={() => restoreSubmission(item)}
                                                    disabled={loading}
                                                    className="btn-secondary text-body-small disabled:opacity-50"
                                                >
                                                    Restore
                                                </button>
                                            </td>
                                        </tr>
                                    ))
                                )}
                            </tbody>
                        </table>
                    </div>
                </div>

                {isModalOpen && (
                    <ModelSelectionModal
                        onSelect={startEnv}
                        onCancel={() => setIsModalOpen(false)}
                    />
                )}

                {loading && <LoadingOverlay message={message} steps={loadingSteps} />}
            </div>
        </div>
    )
}

export default App