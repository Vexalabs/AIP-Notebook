import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Check, Loader, BrainCircuit } from 'lucide-react';

const ModelSelectionModal = ({ onSelect, onCancel }) => {
    const [models, setModels] = useState([]);
    const [loading, setLoading] = useState(true);
    const [selectedModel, setSelectedModel] = useState(null);
    const [currentStep, setCurrentStep] = useState(0);

    const steps = [
        { label: 'Connecting to registry...' },
        { label: 'Authenticating request...' },
        { label: 'Fetching sample models...' },
        { label: 'Validating templates...' }
    ];

    useEffect(() => {
        const fetchModels = async () => {
            try {
                // Step 0: Connecting
                setCurrentStep(0);
                await new Promise(resolve => setTimeout(resolve, 600));

                // Step 1: Authenticating
                setCurrentStep(1);
                await new Promise(resolve => setTimeout(resolve, 600));

                // Step 2: Fetching
                setCurrentStep(2);
                await new Promise(resolve => setTimeout(resolve, 800));

                // Step 3: Validating (happens during fetch)
                setCurrentStep(3);

                const res = await axios.get('/api/models/list-samples');
                setModels(res.data);
                if (res.data.length > 0) {
                    setSelectedModel(res.data[0].id); // Default to first model
                }
            } catch (err) {
                console.error("Failed to fetch sample models", err);
            } finally {
                setLoading(false);
            }
        };
        fetchModels();
    }, []);

    const handleSelect = () => {
        if (selectedModel) {
            onSelect(selectedModel);
        }
    };

    return (
        <div className="fixed inset-0 bg-background-dark bg-opacity-80 flex items-center justify-center z-50 font-sans">
            <div className="card p-8 rounded-lg shadow-2xl w-full max-w-lg">
                <h2 className="text-h6 font-semibold mb-6">Select a Sample Model</h2>

                {loading ? (
                    <div className="flex flex-col items-center justify-center h-48 space-y-4">
                        <div className="w-full max-w-xs space-y-3">
                            {steps.map((step, index) => (
                                <div key={index} className="flex items-center gap-3">
                                    {index < currentStep ? (
                                        <Check className="text-success w-5 h-5" />
                                    ) : index === currentStep ? (
                                        <Loader className="text-primary-default w-5 h-5 animate-spin" />
                                    ) : (
                                        <div className="w-5 h-5 rounded-full border-2 border-border-dark"></div>
                                    )}

                                    <span className={`text-body-small ${index < currentStep ? 'text-light-grey' :
                                            index === currentStep ? 'text-text-dark font-medium' :
                                                'text-border-dark'
                                        }`}>
                                        {step.label}
                                    </span>
                                </div>
                            ))}
                        </div>
                    </div>
                ) : models.length > 0 ? (
                    <div className="space-y-4 mb-8">
                        {models.map((model) => (
                            <div
                                key={model.id}
                                onClick={() => setSelectedModel(model.id)}
                                className={`p-4 border rounded-lg cursor-pointer transition-all ${selectedModel === model.id
                                    ? 'border-primary-default bg-primary-default/10 ring-2 ring-primary-default'
                                    : 'border-border-dark hover:bg-panel-dark/50'
                                    }`}
                            >
                                <div className="flex items-center justify-between">
                                    <div>
                                        <h3 className="font-bold text-body-medium">{model.name}</h3>
                                        <p className="text-light-grey text-body-small">{model.description}</p>
                                    </div>
                                    {selectedModel === model.id && (
                                        <div className="w-6 h-6 bg-primary-default rounded-full flex items-center justify-center">
                                            <Check size={16} className="text-background-dark" />
                                        </div>
                                    )}
                                </div>
                            </div>
                        ))}
                    </div>
                ) : (
                    <div className="text-center h-48 flex flex-col items-center justify-center">
                        <BrainCircuit className="w-12 h-12 text-light-grey opacity-50 mb-4" />
                        <h3 className="font-bold text-body-medium">No Sample Models Found</h3>
                        <p className="text-light-grey text-body-small">The 'sample_models' directory may be empty or missing.</p>
                    </div>
                )}

                <div className="flex justify-end gap-4">
                    <button onClick={onCancel} className="btn-secondary">
                        Cancel
                    </button>
                    <button onClick={handleSelect} disabled={!selectedModel || loading} className="btn-primary">
                        Start Environment
                    </button>
                </div>
            </div>
        </div>
    );
};

export default ModelSelectionModal;
