import { format, parseISO } from 'date-fns';
import type { CalendarEvent, EventCreate } from '../../data/schemas.tsx';

interface EventModalProps {
  isOpen: boolean;
  selectedEvent: CalendarEvent | null;
  newEvent: EventCreate;
  isLoading: boolean;
  onClose: () => void;
  onSave: () => void;
  onDelete: () => void;
  onEventChange: (event: EventCreate) => void;
}

export default function EventModal({
  isOpen,
  selectedEvent,
  newEvent,
  isLoading,
  onClose,
  onSave,
  onDelete,
  onEventChange
}: EventModalProps) {
  if (!isOpen) return null;

  const handleTimeChange = (field: 'start_time' | 'end_time', timeValue: string) => {
    const [hours, minutes] = timeValue.split(':').map(Number);
    const currentDate = new Date(parseISO(newEvent[field]));
    currentDate.setHours(hours, minutes);
    onEventChange({
      ...newEvent,
      [field]: currentDate.toISOString()
    });
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-paper p-6 rounded w-96 border-2 border-gray-800">
        <h3 className="text-xl font-bold mb-4">
          {selectedEvent ? 'Edit Event' : 'Add New Event'}
        </h3>
        
        <div className="mb-4">
          <label className="block mb-1">Title</label>
          <input 
            type="text"
            className="w-full p-2 border border-gray-800"
            value={newEvent.title}
            onChange={(e) => onEventChange({...newEvent, title: e.target.value})}
            disabled={isLoading}
          />
        </div>
        
        <div className="mb-4">
          <label className="block mb-1">Description</label>
          <textarea
            className="w-full p-2 border border-gray-800"
            value={newEvent.description || ''}
            onChange={(e) => onEventChange({...newEvent, description: e.target.value})}
            disabled={isLoading}
          />
        </div>
        
        <div className="flex gap-4 mb-4">
          <div>
            <label className="block mb-1">Start Time</label>
            <input 
              type="time"
              className="p-2 border border-gray-800"
              value={format(parseISO(newEvent.start_time), 'HH:mm')}
              onChange={(e) => handleTimeChange('start_time', e.target.value)}
              disabled={isLoading}
            />
          </div>
          <div>
            <label className="block mb-1">End Time</label>
            <input 
              type="time"
              className="p-2 border border-gray-800"
              value={format(parseISO(newEvent.end_time), 'HH:mm')}
              onChange={(e) => handleTimeChange('end_time', e.target.value)}
              disabled={isLoading}
            />
          </div>
        </div>
        
        <div className="flex justify-between">
          <div>
            {selectedEvent && (
              <button 
                className="px-4 py-2 bg-red-500 text-white disabled:opacity-50"
                onClick={onDelete}
                disabled={isLoading}
              >
                Delete
              </button>
            )}
          </div>
          <div className="flex gap-2">
            <button 
              className="px-4 py-2 border border-gray-800 disabled:opacity-50"
              onClick={onClose}
              disabled={isLoading}
            >
              Cancel
            </button>
            <button 
              className="px-4 py-2 bg-blue text-white disabled:opacity-50"
              onClick={onSave}
              disabled={isLoading || !newEvent.title.trim()}
            >
              {selectedEvent ? 'Update' : 'Create'}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
} 