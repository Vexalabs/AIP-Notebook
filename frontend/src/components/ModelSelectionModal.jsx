import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Check, Loader, BrainCircuit } from 'lucide-react';

const ModelSelectionModal = ({ onSelect, onCancel }) => {
    const [models, setModels] = useState([]);
    const [loading, setLoading] = useState(true);
    const [selectedModel, setSelectedModel] = useState(null);

    useEffect(() => {
        const fetchModels = async () => {
            try {
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
                    <div className="flex items-center justify-center h-48">
                        <Loader className="animate-spin text-primary-default" size={48} />
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
