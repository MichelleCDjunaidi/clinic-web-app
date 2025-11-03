<template>
  <div class="new-consultation">
    <div class="header">
      <h2>New Consultation</h2>
      <router-link to="/consultations" class="btn-secondary">
        ← Back to List
      </router-link>
    </div>

    <form @submit.prevent="handleSubmit" class="consultation-form">
      <div class="form-row">
        <div class="form-group">
          <label for="patient_name">Patient Name *</label>
          <input
            id="patient_name"
            v-model="form.patient_name"
            type="text"
            required
            placeholder="Enter patient name"
            class="form-input"
          />
        </div>

        <div class="form-group">
          <label for="consultation_date">Consultation Date *</label>
          <input
            id="consultation_date"
            v-model="form.consultation_date"
            type="date"
            required
            class="form-input"
          />
        </div>
      </div>

      <div class="form-group">
        <label for="notes">Notes ({{ form.notes?.length || 0 }}/5000)</label>
        <textarea
          id="notes"
          v-model="form.notes"
          rows="4"
          maxlength="5000"
          placeholder="Enter consultation notes..."
          class="form-textarea"
        ></textarea>
      </div>

      <div class="form-group">
        <label for="diagnosis_search">Search Diagnosis Codes *</label>
        <input
          id="diagnosis_search"
          v-model="searchTerm"
          @input="searchDiagnosis"
          type="text"
          placeholder="Type at least two letters to search ICD-10 codes..."
          class="form-input"
        />

        <div v-if="searchResults.length > 0" class="search-results">
          <div
            v-for="diagnosis in searchResults"
            :key="diagnosis.id"
            @click="addDiagnosis(diagnosis)"
            class="search-result-item"
          >
            <span class="diagnosis-code">{{ diagnosis.code }}</span>
            <span class="diagnosis-desc">{{ diagnosis.description }}</span>
          </div>
        </div>
      </div>

      <div class="form-group">
        <label>Selected Diagnosis Codes</label>
        <div v-if="selectedDiagnoses.length === 0" class="empty-selection">
          No diagnosis codes selected. Search and click to add.
        </div>
        <div v-else class="selected-diagnoses">
          <div
            v-for="diagnosis in selectedDiagnoses"
            :key="diagnosis.code"
            class="selected-diagnosis"
          >
            <span class="diagnosis-code">{{ diagnosis.code }}</span>
            <span class="diagnosis-desc">{{ diagnosis.description }}</span>
            <button
              type="button"
              @click="removeDiagnosis(diagnosis.code)"
              class="remove-btn"
            >
              ×
            </button>
          </div>
        </div>
      </div>

      <div v-if="error" class="error-message">
        {{ error }}
      </div>

      <div v-if="success" class="success-message">
        Consultation created successfully!
      </div>

      <div class="form-actions">
        <button
          type="submit"
          :disabled="loading || selectedDiagnoses.length === 0"
          class="btn-submit"
        >
          {{ loading ? "Creating..." : "Create Consultation" }}
        </button>
      </div>
    </form>
  </div>
</template>

<script>
import { ref, reactive } from "vue";
import { useRouter } from "vue-router";
import api from "../api/api";

export default {
  name: "NewConsultation",
  setup() {
    const router = useRouter();
    const searchTerm = ref("");
    const searchResults = ref([]);
    const selectedDiagnoses = ref([]);
    const loading = ref(false);
    const error = ref("");
    const success = ref(false);

    const form = reactive({
      patient_name: "",
      consultation_date: new Date().toISOString().split("T")[0],
      notes: "",
    });

    let searchTimeout = null;

    const searchDiagnosis = () => {
      if (searchTimeout) clearTimeout(searchTimeout);

      if (searchTerm.value.length < 2) {
        searchResults.value = [];
        return;
      }

      searchTimeout = setTimeout(async () => {
        try {
          const response = await api.searchDiagnosis(searchTerm.value);
          searchResults.value = response.data;
        } catch (err) {
          console.error("Search failed:", err);
        }
      }, 300);
    };

    const addDiagnosis = (diagnosis) => {
      if (!selectedDiagnoses.value.find((d) => d.code === diagnosis.code)) {
        selectedDiagnoses.value.push(diagnosis);
      }
      searchTerm.value = "";
      searchResults.value = [];
    };

    const removeDiagnosis = (code) => {
      selectedDiagnoses.value = selectedDiagnoses.value.filter(
        (d) => d.code !== code
      );
    };

    const handleSubmit = async () => {
      // Frontend validation
      error.value = "";

      // Validate patient name
      if (!form.patient_name || form.patient_name.trim().length < 2) {
        error.value = "Patient name must be at least 2 characters";
        return;
      }

      if (form.patient_name.trim().length > 255) {
        error.value = "Patient name must be less than 255 characters";
        return;
      }

      // Validate consultation date
      const selectedDate = new Date(form.consultation_date);
      const today = new Date();
      selectedDate.setHours(0, 0, 0, 0);
      today.setHours(0, 0, 0, 0);
      if (selectedDate > today) {
        error.value = "Consultation date cannot be in the future";
        return;
      }

      // Validate diagnosis codes
      if (selectedDiagnoses.value.length === 0) {
        error.value = "Please select at least one diagnosis code";
        return;
      }

      if (selectedDiagnoses.value.length > 20) {
        error.value = "Maximum 20 diagnosis codes allowed";
        return;
      }

      // Validate notes length
      if (form.notes && form.notes.length > 5000) {
        error.value = "Notes must be less than 5000 characters";
        return;
      }

      success.value = false;
      loading.value = true;

      try {
        const data = {
          patient_name: form.patient_name.trim(),
          consultation_date: form.consultation_date,
          notes: form.notes?.trim() || null,
          diagnosis_codes: selectedDiagnoses.value.map((d) => d.code),
        };

        await api.createConsultation(data);
        success.value = true;

        setTimeout(() => {
          router.push("/consultations");
        }, 1500);
      } catch (err) {
        // Handle validation errors from backend
        if (err.response?.status === 422) {
          const errors = err.response.data.errors;
          if (Array.isArray(errors)) {
            error.value = errors.join("; ");
          } else {
            error.value = err.response.data.detail || "Validation failed";
          }
        } else {
          error.value =
            err.response?.data?.detail || "Failed to create consultation";
        }
      } finally {
        loading.value = false;
      }
    };

    return {
      form,
      searchTerm,
      searchResults,
      selectedDiagnoses,
      loading,
      error,
      success,
      searchDiagnosis,
      addDiagnosis,
      removeDiagnosis,
      handleSubmit,
    };
  },
};
</script>

<style scoped>
.new-consultation {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.header h2 {
  font-size: 1.8rem;
  color: #2c3e50;
}

.btn-secondary {
  background: #95a5a6;
  color: white;
  padding: 0.75rem 1.5rem;
  border-radius: 6px;
  text-decoration: none;
  font-weight: 500;
  transition: background 0.3s;
}

.btn-secondary:hover {
  background: #7f8c8d;
}

.consultation-form {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.5rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  position: relative;
}

.form-group label {
  font-weight: 500;
  color: #2c3e50;
  font-size: 0.95rem;
}

.form-input,
.form-textarea {
  padding: 0.75rem;
  border: 2px solid #e0e0e0;
  border-radius: 6px;
  font-size: 1rem;
  font-family: inherit;
  transition: border-color 0.3s;
}

.form-input:focus,
.form-textarea:focus {
  outline: none;
  border-color: #3498db;
}

.search-results {
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  background: white;
  border: 2px solid #e0e0e0;
  border-top: none;
  border-radius: 0 0 6px 6px;
  max-height: 300px;
  overflow-y: auto;
  z-index: 10;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.search-result-item {
  padding: 0.75rem;
  cursor: pointer;
  display: flex;
  gap: 0.75rem;
  align-items: center;
  transition: background 0.2s;
}

.search-result-item:hover {
  background: #f8f9fa;
}

.diagnosis-code {
  background: #e3f2fd;
  color: #1976d2;
  padding: 0.25rem 0.75rem;
  border-radius: 4px;
  font-weight: 600;
  font-size: 0.85rem;
  min-width: 60px;
  text-align: center;
}

.diagnosis-desc {
  color: #2c3e50;
  flex: 1;
}

.empty-selection {
  padding: 1rem;
  background: #f8f9fa;
  border-radius: 6px;
  color: #7f8c8d;
  text-align: center;
}

.selected-diagnoses {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.selected-diagnosis {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem;
  background: #f8f9fa;
  border-radius: 6px;
  border: 2px solid #e0e0e0;
}

.remove-btn {
  background: #e74c3c;
  color: white;
  border: none;
  width: 28px;
  height: 28px;
  border-radius: 50%;
  cursor: pointer;
  font-size: 1.2rem;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background 0.3s;
  margin-left: auto;
}

.remove-btn:hover {
  background: #c0392b;
}

.error-message {
  background: #fee;
  color: #c33;
  padding: 1rem;
  border-radius: 6px;
}

.success-message {
  background: #e8f5e9;
  color: #2e7d32;
  padding: 1rem;
  border-radius: 6px;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  margin-top: 1rem;
}

.btn-submit {
  background: #27ae60;
  color: white;
  border: none;
  padding: 0.875rem 2rem;
  border-radius: 6px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.3s, transform 0.2s;
}

.btn-submit:hover:not(:disabled) {
  background: #229954;
  transform: translateY(-2px);
}

.btn-submit:disabled {
  background: #95a5a6;
  cursor: not-allowed;
}

@media (max-width: 768px) {
  .form-row {
    grid-template-columns: 1fr;
  }
}
</style>
