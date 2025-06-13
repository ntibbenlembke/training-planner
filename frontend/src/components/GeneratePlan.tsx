import { useState } from 'react';
import { buildApiUrl } from '../config/api';

interface PlannerPreferences {
  frequency_per_week: number;
  preferred_time_of_day: string;
  workout_duration_minutes: number;
  padding_before_minutes: number;
  padding_after_minutes: number;
  workout_types: string[];
  difficulty_level: string;
  days_of_week: string[];
}

export default function GeneratePlan() {
  const [preferences, setPreferences] = useState<PlannerPreferences>({
    frequency_per_week: 3,
    preferred_time_of_day: 'morning',
    workout_duration_minutes: 60,
    padding_before_minutes: 15,
    padding_after_minutes: 15,
    workout_types: ['cycling'],
    difficulty_level: 'moderate',
    days_of_week: []
  });

  const [isGenerating, setIsGenerating] = useState(false);
  const [message, setMessage] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  // Current user ID
  const userId = 3;

  const handlePreferenceChange = (field: keyof PlannerPreferences, value: string | number | string[]) => {
    setPreferences(prev => ({
      ...prev,
      [field]: value
    }));
  };

  const handleWorkoutTypeChange = (type: string, checked: boolean) => {
    setPreferences(prev => ({
      ...prev,
      workout_types: checked 
        ? [...prev.workout_types, type]
        : prev.workout_types.filter(t => t !== type)
    }));
  };

  const handleDayOfWeekChange = (day: string, checked: boolean) => {
    setPreferences(prev => ({
      ...prev,
      days_of_week: checked
        ? [...prev.days_of_week, day]
        : prev.days_of_week.filter(d => d !== day)
    }));
  };

  const generatePlan = async () => {
    try {
      setIsGenerating(true);
      setError(null);
      setMessage(null);

      const response = await fetch(buildApiUrl('/planner/create-training-plan', userId), {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          user_id: userId,
          ...preferences
        }),
      });

      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(`Failed to generate plan: ${response.status} ${errorText}`);
      }

      const result = await response.json();
      setMessage('Training plan generated successfully!');
      console.log('Generated plan:', result);
      
      // Optionally refresh the calendar to show new events
      window.location.reload();
      
    } catch (err) {
      setError('Error generating plan: ' + (err instanceof Error ? err.message : String(err)));
      console.error('Error generating plan:', err);
    } finally {
      setIsGenerating(false);
    }
  };

  const workoutTypes = ['cycling', 'running', 'strength_training', 'yoga', 'swimming'];
  const daysOfWeek = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'];
  const timeOptions = ['morning', 'afternoon', 'evening'];
  const difficultyLevels = ['easy', 'moderate', 'hard', 'expert'];

  return (
    <div className="bg-paper border-2 border-gray-800 mx-4 mt-4 p-4">
      <h1 className="text-xl font-bold mb-4">Generate Training Plan</h1>

      {/* Frequency */}
      <div className="mb-4">
        <label className="block mb-1 font-semibold">Workouts per Week</label>
        <input
          type="number"
          min="1"
          max="7"
          className="w-full p-2 border border-gray-800"
          value={preferences.frequency_per_week}
          onChange={(e) => handlePreferenceChange('frequency_per_week', parseInt(e.target.value))}
        />
      </div>

      {/* Preferred Time */}
      <div className="mb-4">
        <label className="block mb-1 font-semibold">Preferred Time of Day</label>
        <select
          className="w-full p-2 border border-gray-800"
          value={preferences.preferred_time_of_day}
          onChange={(e) => handlePreferenceChange('preferred_time_of_day', e.target.value)}
        >
          {timeOptions.map(time => (
            <option key={time} value={time}>
              {time.charAt(0).toUpperCase() + time.slice(1)}
            </option>
          ))}
        </select>
      </div>

      {/* Workout Duration */}
      <div className="mb-4">
        <label className="block mb-1 font-semibold">Workout Duration (minutes)</label>
        <input
          type="number"
          min="15"
          max="180"
          step="15"
          className="w-full p-2 border border-gray-800"
          value={preferences.workout_duration_minutes}
          onChange={(e) => handlePreferenceChange('workout_duration_minutes', parseInt(e.target.value))}
        />
      </div>

      {/* Padding Times */}
      <div className="grid grid-cols-2 gap-4 mb-4">
        <div>
          <label className="block mb-1 font-semibold">Prep Time (minutes)</label>
          <input
            type="number"
            min="0"
            max="60"
            step="5"
            className="w-full p-2 border border-gray-800"
            value={preferences.padding_before_minutes}
            onChange={(e) => handlePreferenceChange('padding_before_minutes', parseInt(e.target.value))}
          />
        </div>
        <div>
          <label className="block mb-1 font-semibold">Cool Down (minutes)</label>
          <input
            type="number"
            min="0"
            max="60"
            step="5"
            className="w-full p-2 border border-gray-800"
            value={preferences.padding_after_minutes}
            onChange={(e) => handlePreferenceChange('padding_after_minutes', parseInt(e.target.value))}
          />
        </div>
      </div>

      {/* Workout Types */}
      <div className="mb-4">
        <label className="block mb-2 font-semibold">Workout Types</label>
        <div className="grid grid-cols-2 gap-2">
          {workoutTypes.map(type => (
            <label key={type} className="flex items-center">
              <input
                type="checkbox"
                className="mr-2"
                checked={preferences.workout_types.includes(type)}
                onChange={(e) => handleWorkoutTypeChange(type, e.target.checked)}
              />
              <span className="text-sm">{type.replace('_', ' ').toUpperCase()}</span>
            </label>
          ))}
        </div>
      </div>

      {/* Difficulty Level */}
      <div className="mb-4">
        <label className="block mb-1 font-semibold">Difficulty Level</label>
        <select
          className="w-full p-2 border border-gray-800"
          value={preferences.difficulty_level}
          onChange={(e) => handlePreferenceChange('difficulty_level', e.target.value)}
        >
          {difficultyLevels.map(level => (
            <option key={level} value={level}>
              {level.charAt(0).toUpperCase() + level.slice(1)}
            </option>
          ))}
        </select>
      </div>

      {/* Preferred Days */}
      <div className="mb-6">
        <label className="block mb-2 font-semibold">Preferred Days (optional)</label>
        <div className="grid grid-cols-2 gap-2">
          {daysOfWeek.map(day => (
            <label key={day} className="flex items-center">
              <input
                type="checkbox"
                className="mr-2"
                checked={preferences.days_of_week.includes(day)}
                onChange={(e) => handleDayOfWeekChange(day, e.target.checked)}
              />
              <span className="text-sm">{day.charAt(0).toUpperCase() + day.slice(1)}</span>
            </label>
          ))}
        </div>
      </div>

      {/* Status Messages */}
      {message && (
        <div className="mb-4 p-3 bg-green-100 border border-green-400 text-green-700 rounded">
          {message}
        </div>
      )}
      
      {error && (
        <div className="mb-4 p-3 bg-red-100 border border-red-400 text-red-700 rounded">
          {error}
        </div>
      )}

      {/* Generate Button */}
      <button
        onClick={generatePlan}
        disabled={isGenerating || preferences.workout_types.length === 0}
        className={`w-full py-4 text-lg font-bold border-2 transition-colors ${
          isGenerating || preferences.workout_types.length === 0
            ? 'bg-gray-300 border-gray-400 text-gray-500 cursor-not-allowed'
            : 'bg-blue text-white border-blue hover:bg-blue-dark hover:border-blue-dark'
        }`}
      >
        {isGenerating ? 'Generating Plan...' : 'GENERATE TRAINING PLAN'}
      </button>
    </div>
  );
}