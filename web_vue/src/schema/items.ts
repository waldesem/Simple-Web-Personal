import { Component, h } from 'vue';
import type { AccordionItem, TableColumn, TabsItem } from '@nuxt/ui';
import { Conclusions, Decisions, type Items, type Person } from '@/types';

type NavigationItem = AccordionItem & TabsItem;

export interface Navigations extends NavigationItem {
  label: string;
  slot: keyof Items;
}

export const tabs = [
  { label: 'Проверки', icon: 'i-lucide-file-check', slot: 'checks' },
  { label: 'Полиграф', icon: 'i-lucide-heart-pulse', slot: 'poligrafs' },
  { label: 'Расследования', icon: 'i-lucide-archive', slot: 'investigations' },
  { label: 'Запросы', icon: 'i-lucide-file-question-mark', slot: 'inquiries' },
] as Navigations[];

export const accordion = [
  { label: 'Должности', icon: 'i-lucide-briefcase-business', slot: 'staffs' },
  { label: 'Образование', icon: 'i-lucide-graduation-cap', slot: 'educations' },
  { label: 'Работа', icon: 'i-lucide-construction', slot: 'workplaces' },
  { label: 'Документы', icon: 'i-lucide-book-check', slot: 'documents' },
  { label: 'Адреса', icon: 'i-lucide-house', slot: 'addresses' },
  { label: 'Контакты', icon: 'i-lucide-phone', slot: 'contacts' },
  { label: 'Изменения имени', icon: 'i-lucide-save-pen', slot: 'previous' },
  {
    label: 'Аффилированность',
    icon: 'i-lucide-chart-pie',
    slot: 'affilations',
  },
] as Navigations[];

export function localStr(str: string): string {
  try {
    return str ? new Date(str).toLocaleDateString() : '';
  } catch {
    return '';
  }
}

function timeAgoStr(str: string) {
  const diff = Date.now() - new Date(str).getTime();
  const diffSec = Math.floor(diff / 1000);
  // Меньше минуты
  if (diffSec < 60) {
    return 'Менее минуты назад';
  }
  // Меньше часа (но больше минуты)
  const diffMin = Math.floor(diffSec / 60);
  if (diffMin < 60) {
    return 'Менее часа назад';
  }
  // Менее суток (но больше часа)
  const diffHours = Math.floor(diffMin / 60);
  if (diffHours < 24) {
    return diffHours + ' часов назад';
  }
  const diffDays = Math.floor(diffHours / 24);
  // Менее недели (но больше суток)
  if (diffDays < 7) {
    return diffDays + ' дней назад';
  }
  if (diffDays < 30) {
    // Менее месяца (но больше недели)
    return Math.floor(diffDays / 7) + ' недели назад';
  }
  // Менее года (но больше месяца)
  if (diffDays < 365) {
    return Math.floor(diffDays / 30) + ' месяцев назад';
  }
  // Больше года
  return Math.floor(diffDays / 365) + ' года назад';
}

export const columns: TableColumn<Person>[] = [
  {
    accessorKey: 'id',
    header: '#',
    meta: { class: { th: 'w-2/23' } },
  },
  {
    accessorKey: 'surname',
    header: 'Фамилия',
    meta: { class: { th: 'w-5/23' } },
  },
  {
    accessorKey: 'firstname',
    header: 'Имя',
    meta: { class: { th: 'w-5/23' } },
  },
  {
    accessorKey: 'patronymic',
    header: 'Отчество',
    meta: { class: { th: 'w-5/23' } },
  },
  {
    accessorKey: 'birthday',
    header: 'Дата рождения',
    meta: { class: { th: 'w-3/23' } },
    cell: ({ row }) => localStr(row.original.birthday),
  },
  {
    accessorKey: 'created',
    header: 'Обновлено',
    meta: { class: { th: 'w-3/23' } },
    cell: ({ row }) => timeAgoStr(row.original.created),
  },
];

type ItemFields<T> = {
  key: keyof T;
  label: string;
  slot?: boolean;
  foo?: (row: T) => string;
  component?: (row: T) => Component;
};

export const person = [
  { key: 'surname', label: 'Фамилия' },
  { key: 'firstname', label: 'Имя' },
  { key: 'patronymic', label: 'Отчество' },
  {
    key: 'birthday',
    label: 'Дата рождения',
    foo: (row) => localStr(row.birthday),
  },
  { key: 'birthplace', label: 'Место рождения' },
  { key: 'citizenship', label: 'Гражданство' },
  { key: 'dual', label: 'Двойное гражданство' },
  { key: 'snils', label: 'СНИЛС' },
  { key: 'inn', label: 'ИНН' },
  { key: 'marital', label: 'Семейное положение' },
  { key: 'addition', label: 'Дополнительная информация' },
  { key: 'created', label: 'Дата записи', foo: (row) => localStr(row.created) },
  { key: 'destination', label: 'Материалы проверок', slot: true },
] as ItemFields<Person>[];

const addresses = [
  { key: 'view', label: 'Вид адреса' },
  { key: 'address', label: 'Адрес' },
] as ItemFields<Items['addresses']>[];

const affilations = [
  { key: 'view', label: 'Вид участия' },
  { key: 'organization', label: 'Организация' },
  { key: 'inn', label: 'ИНН' },
  { key: 'activity', label: 'Деятельность' },
] as ItemFields<Items['affilations']>[];

const checks = [
  { key: 'workplace', label: 'Проверка по местам работы' },
  { key: 'document', label: 'Проверка документов' },
  { key: 'debt', label: 'Проверка задолженностей' },
  { key: 'bankruptcy', label: 'Проверка банкротства' },
  { key: 'bki', label: 'Проверка Кредитной истории' },
  { key: 'courts', label: 'Проверка судебных дел' },
  { key: 'affilation', label: 'Проверка аффилированности' },
  { key: 'terrorist', label: 'Проверка в списке террористов' },
  { key: 'internet', label: 'Проверка в открытых источниках' },
  { key: 'cronos', label: 'Проверка в Кронос' },
  { key: 'addition', label: 'Дополнительная информация' },
  { key: 'comment', label: 'Комментарий' },
  {
    key: 'conclusion',
    label: 'Результат',
    component: (row) => {
      const color =
        row.conclusion === Conclusions.agreed
          ? 'bg-green-500'
          : row.conclusion === Conclusions.cancel
            ? 'bg-gray-500'
            : row.conclusion === Conclusions.comments
              ? 'bg-blue-500'
              : 'bg-red-500';
      return h(
        'span',
        {
          class: [
            'flex inline-flex Items-center py-1 px-2 rounded-md text-sm text-white',
            color,
          ],
        },
        row.conclusion
      );
    },
  },
  { key: 'created', label: 'Дата записи', foo: (row) => localStr(row.created) },
] as ItemFields<Items['checks']>[];

const contacts = [
  { key: 'view', label: 'Вид контакта' },
  { key: 'contact', label: 'Контакт' },
] as ItemFields<Items['contacts']>[];

const documents = [
  { key: 'view', label: 'Вид документа' },
  { key: 'series', label: 'Серия документа' },
  { key: 'digits', label: 'Номер документа' },
  { key: 'agency', label: 'Кем выдан' },
  { key: 'issue', label: 'Дата выдачи', foo: (row) => localStr(row.issue) },
] as ItemFields<Items['documents']>[];

const educations = [
  { key: 'view', label: 'Вид образования' },
  { key: 'institution', label: 'Учебное заведение' },
  { key: 'finished', label: 'Год окончания' },
  { key: 'specialty', label: 'Специальность' },
] as ItemFields<Items['educations']>[];

const inquiries = [
  { key: 'info', label: 'Информация' },
  { key: 'initiator', label: 'Инициатор' },
  { key: 'created', label: 'Дата записи', foo: (row) => localStr(row.created) },
] as ItemFields<Items['inquiries']>[];

const investigations = [
  { key: 'theme', label: 'Тема проверки' },
  { key: 'info', label: 'Информация' },
  { key: 'created', label: 'Дата записи', foo: (row) => localStr(row.created) },
] as ItemFields<Items['investigations']>[];

const poligrafs = [
  { key: 'theme', label: 'Тема проверки' },
  { key: 'results', label: 'Результат' },
  {
    key: 'conclusion',
    label: 'Результат',
    component: (row) => {
      const color =
        row.conclusion === Decisions.agreed
          ? 'bg-green-500'
          : row.conclusion === Decisions.cancel
            ? 'bg-gray-500'
            : row.conclusion === Decisions.comments
              ? 'bg-blue-500'
              : 'bg-red-500';
      return h(
        'span',
        {
          class: [
            'flex inline-flex Items-center py-1 px-2 rounded-md text-sm text-white',
            color,
          ],
        },
        row.conclusion
      );
    },
  },
  { key: 'created', label: 'Дата записи', foo: (row) => localStr(row.created) },
] as ItemFields<Items['poligrafs']>[];

const previous = [
  { key: 'surname', label: 'Фамилия' },
  { key: 'firstname', label: 'Имя' },
  { key: 'patronymic', label: 'Отчество' },
  { key: 'changed', label: 'Год изменения' },
  { key: 'reason', label: 'Причина' },
] as ItemFields<Items['previous']>[];

const staffs = [
  { key: 'position', label: 'Должность' },
  { key: 'department', label: 'Подразделение' },
] as ItemFields<Items['staffs']>[];

const workplaces = [
  { key: 'starts', label: 'Начало работы', foo: (row) => localStr(row.starts) },
  {
    key: 'finished',
    label: 'Окончание работы',
    foo: (row) => localStr(row.finished),
  },
  { key: 'workplace', label: 'Место работы' },
  { key: 'position', label: 'Должность' },
  { key: 'address', label: 'Адрес организации' },
  { key: 'reason', label: 'Причина увольнения' },
] as ItemFields<Items['workplaces']>[];

export const itemsFields = {
  addresses,
  affilations,
  checks,
  contacts,
  documents,
  educations,
  inquiries,
  investigations,
  poligrafs,
  previous,
  staffs,
  workplaces,
};
