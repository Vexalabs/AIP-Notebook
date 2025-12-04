import React, { useState, useEffect } from 'react'
import { BrainCircuit, CheckCircle2, Circle, Loader2 } from 'lucide-react'

const LoadingOverlay = ({ message, steps = [] }) => {
    // If no steps provided, use default generic steps based on message
    const defaultSteps = steps.length > 0 ? steps : [
        { label: 'Initializing request...', status: 'completed' },
        { label: message || 'Processing...', status: 'processing' },
        { label: 'Finalizing...', status: 'pending' }
    ]

    const [currentSteps, setCurrentSteps] = useState(defaultSteps)

    // Simulate step progression if generic steps are used
    useEffect(() => {
        if (steps.length === 0) {
            const timer1 = setTimeout(() => {
                setCurrentSteps(prev => [
                    { ...prev[0], status: 'completed' },
                    { ...prev[1], status: 'processing' },
                    { ...prev[2], status: 'pending' }
                ])
            }, 500)

            const timer2 = setTimeout(() => {
                setCurrentSteps(prev => [
                    { ...prev[0], status: 'completed' },
                    { ...prev[1], status: 'completed' },
                    { ...prev[2], status: 'processing' }
                ])
            }, 2000)

            return () => {
                clearTimeout(timer1)
                clearTimeout(timer2)
            }
        } else {
            setCurrentSteps(steps)
        }
    }, [steps, message])

    return (
        <div className="fixed inset-0 bg-background-dark/80 backdrop-blur-sm z-50 flex items-center justify-center">
            <div className="flex flex-col w-full max-w-md p-8 rounded-2xl bg-panel-dark border border-border-dark shadow-2xl animate-in fade-in zoom-in duration-300">

                <div className="flex items-center gap-4 mb-6 border-b border-border-dark pb-6">
                    <div className="relative">
                        <div className="absolute inset-0 rounded-full border-2 border-primary-default/30 border-t-primary-default animate-spin w-12 h-12"></div>
                        <div className="w-12 h-12 flex items-center justify-center text-primary-default">
                            <BrainCircuit size={24} />
                        </div>
                    </div>
                    <div>
                        <h3 className="text-h6 font-bold text-text-dark">Processing Request</h3>
                        <p className="text-body-small text-light-grey">Please wait while we set things up</p>
                    </div>
                </div>

                <div className="space-y-4">
                    {currentSteps.map((step, index) => (
                        <div key={index} className="flex items-center gap-3">
                            {step.status === 'completed' ? (
                                <CheckCircle2 className="text-success w-5 h-5 shrink-0" />
                            ) : step.status === 'processing' ? (
                                <Loader2 className="text-primary-default w-5 h-5 animate-spin shrink-0" />
                            ) : (
                                <Circle className="text-border-dark w-5 h-5 shrink-0" />
                            )}

                            <span className={`text-body-small ${step.status === 'completed' ? 'text-light-grey' :
                                    step.status === 'processing' ? 'text-text-dark font-medium' :
                                        'text-border-dark'
                                }`}>
                                {step.label}
                            </span>
                        </div>
                    ))}
                </div>
            </div>
        </div>
    )
}

export default LoadingOverlay
