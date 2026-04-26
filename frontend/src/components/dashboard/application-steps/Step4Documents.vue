<template>
  <div class="gc-step4">
    <header class="gc-step-section-header">
      <h3 class="gc-step-section-title">{{ t('dashboard.edit.documentsStep.heading') }}</h3>
      <p class="gc-step-section-sub">{{ t('dashboard.edit.documentsStep.subheading') }}</p>
    </header>

    <div class="gc-uploader">
      <div class="gc-uploader-row">
        <q-select
          v-model="selectedKind"
          :options="kindOptions"
          outlined
          dense
          emit-value
          map-options
          :label="t('dashboard.edit.documentsStep.kind')"
          class="gc-uploader-kind"
        />

        <q-file
          v-model="pendingFile"
          outlined
          dense
          accept=".pdf,.jpg,.jpeg,.png"
          :max-file-size="25 * 1024 * 1024"
          class="gc-uploader-input"
          :label="t('dashboard.edit.documentsStep.addButton')"
          @update:model-value="onFileSelected"
        >
          <template #prepend>
            <q-icon name="attach_file" />
          </template>
        </q-file>
      </div>

      <p class="gc-uploader-hint">{{ t('dashboard.edit.documentsStep.maxSize') }}</p>

      <q-banner v-if="error" class="gc-error-banner" dense rounded>{{ error }}</q-banner>
    </div>

    <div v-if="documents.length === 0 && !uploading" class="gc-docs-empty">
      <q-icon name="description" size="32px" />
      <span>{{ t('dashboard.edit.documentsStep.empty') }}</span>
    </div>

    <ul v-else class="gc-docs-list">
      <li v-for="doc in documents" :key="doc.id" class="gc-doc-item">
        <div class="gc-doc-icon">
          <q-icon :name="iconForKind(doc.kind)" size="20px" />
        </div>
        <div class="gc-doc-text">
          <span class="gc-doc-title">{{ doc.original_filename }}</span>
          <span class="gc-doc-meta">
            {{ kindLabel(doc.kind) }} • {{ formatBytes(doc.size_bytes) }}
            <span
              class="gc-doc-status"
              :class="doc.is_verified ? 'gc-doc-status-verified' : 'gc-doc-status-pending'"
            >
              {{
                doc.is_verified
                  ? t('dashboard.edit.documentsStep.verified')
                  : t('dashboard.edit.documentsStep.pending')
              }}
            </span>
          </span>
        </div>
        <q-btn
          flat
          dense
          icon="close"
          :loading="removingId === doc.id"
          :title="t('dashboard.edit.documentsStep.remove')"
          class="gc-doc-remove"
          @click="onRemove(doc.id)"
        />
      </li>

      <li v-if="uploading" class="gc-doc-item gc-doc-uploading">
        <q-spinner size="20px" color="primary" />
        <span class="gc-doc-uploading-text">{{ t('dashboard.edit.documentsStep.uploading') }}</span>
      </li>
    </ul>
  </div>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue';
import { useI18n } from 'vue-i18n';
import {
  applicationsService,
  type ApplicationDocument,
  type DocumentKind,
} from 'src/services/applications';
import { extractApiError } from 'src/utils/api-errors';

interface Props {
  reference: string;
  documents: ApplicationDocument[];
}

const props = defineProps<Props>();
const emit = defineEmits<{ 'documents-changed': [] }>();

const { t } = useI18n();

const pendingFile = ref<File | null>(null);
const selectedKind = ref<DocumentKind>('passport');
const uploading = ref(false);
const removingId = ref<number | null>(null);
const error = ref<string | null>(null);

const kindOptions = computed<{ label: string; value: DocumentKind }[]>(() => [
  { label: t('dashboard.edit.documentsStep.kinds.passport'), value: 'passport' },
  { label: t('dashboard.edit.documentsStep.kinds.transcript'), value: 'transcript' },
  { label: t('dashboard.edit.documentsStep.kinds.cv'), value: 'cv' },
  { label: t('dashboard.edit.documentsStep.kinds.financial'), value: 'financial' },
  { label: t('dashboard.edit.documentsStep.kinds.certificate'), value: 'certificate' },
  { label: t('dashboard.edit.documentsStep.kinds.photo'), value: 'photo' },
  { label: t('dashboard.edit.documentsStep.kinds.other'), value: 'other' },
]);

function kindLabel(kind: DocumentKind): string {
  return t(`dashboard.edit.documentsStep.kinds.${kind}`);
}

function iconForKind(kind: DocumentKind): string {
  const map: Record<DocumentKind, string> = {
    passport: 'badge',
    transcript: 'school',
    cv: 'work',
    financial: 'account_balance',
    certificate: 'verified',
    photo: 'image',
    other: 'description',
  };
  return map[kind];
}

function formatBytes(bytes: number): string {
  if (bytes < 1024) return `${bytes} B`;
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(0)} KB`;
  return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
}

async function onFileSelected(file: File | null) {
  if (!file) return;
  error.value = null;
  uploading.value = true;
  try {
    await applicationsService.uploadDocument(props.reference, file, selectedKind.value);
    emit('documents-changed');
  } catch (err) {
    error.value = extractApiError(err, t('dashboard.edit.documentsStep.uploadError'));
  } finally {
    uploading.value = false;
    pendingFile.value = null;
  }
}

async function onRemove(documentId: number) {
  if (!window.confirm(t('dashboard.edit.documentsStep.removeConfirm'))) return;
  error.value = null;
  removingId.value = documentId;
  try {
    await applicationsService.deleteDocument(props.reference, documentId);
    emit('documents-changed');
  } catch (err) {
    error.value = extractApiError(err, t('errors.generic'));
  } finally {
    removingId.value = null;
  }
}
</script>

<style scoped lang="scss">
.gc-step4 {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.gc-step-section-header {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.gc-step-section-title {
  font-size: 18px;
  font-weight: 700;
  letter-spacing: -0.01em;
  margin: 0;
}

.gc-step-section-sub {
  font-size: 13px;
  color: var(--gc-text-muted);
  margin: 0;
}

.gc-uploader {
  background: var(--gc-bg-soft);
  border-radius: var(--gc-radius-md);
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.gc-uploader-row {
  display: flex;
  flex-direction: column;
  gap: 12px;

  @media (min-width: 600px) {
    flex-direction: row;
    align-items: flex-start;
  }
}

.gc-uploader-kind {
  flex: 0 0 200px;
}

.gc-uploader-input {
  flex: 1;
}

.gc-uploader-hint {
  font-size: 12px;
  color: var(--gc-text-muted);
  margin: 0;
}

.gc-docs-empty {
  border: 1px dashed var(--gc-border);
  border-radius: var(--gc-radius-md);
  padding: 32px;
  text-align: center;
  color: var(--gc-text-muted);
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  font-size: 13px;
}

.gc-docs-list {
  list-style: none;
  margin: 0;
  padding: 0;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.gc-doc-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 14px;
  border-radius: var(--gc-radius-md);
  background: var(--gc-bg);
  border: 1px solid var(--gc-border);
}

.gc-doc-icon {
  width: 36px;
  height: 36px;
  border-radius: 10px;
  background: var(--gc-bg-soft);
  color: var(--gc-primary);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.gc-doc-text {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 2px;
  min-width: 0;
}

.gc-doc-title {
  font-size: 14px;
  font-weight: 600;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.gc-doc-meta {
  font-size: 12px;
  color: var(--gc-text-muted);
  display: inline-flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 8px;
}

.gc-doc-status {
  font-size: 10px;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  padding: 2px 8px;
  border-radius: var(--gc-radius-pill);
  font-weight: 600;
}

.gc-doc-status-verified {
  background: rgba(34, 175, 110, 0.14);
  color: #1f9b62;
}

.gc-doc-status-pending {
  background: rgba(150, 150, 150, 0.12);
  color: var(--gc-text-muted);
}

.gc-doc-remove {
  flex-shrink: 0;
  color: var(--gc-text-muted);

  &:hover {
    color: #d04848;
  }
}

.gc-doc-uploading {
  justify-content: center;
  background: var(--gc-bg-soft);
  border-style: dashed;
}

.gc-doc-uploading-text {
  font-size: 13px;
  color: var(--gc-text-muted);
}
</style>
