import { localStr, timeAgoStr } from "@/utils";
import type { ItemsAccordionTabs, Person, TableColumns } from "@/types";

export const tableCols: TableColumns<Person>[] = [
  {
    name: "id",
    header: "#",
  },
  {
    name: "surname",
    header: "Фамилия",
  },
  {
    name: "firstname",
    header: "Имя",
  },
  {
    name: "patronymic",
    header: "Отчество",
  },
  {
    name: "birthday",
    header: "Дата рождения",
    cell: (row) => localStr(row.birthday),
  },
  {
    name: "created",
    header: "Обновлено",
    cell: (row) => timeAgoStr(row.created),
  },
];

export const anketaTab = {
  label: "Анкета",
  icon: "i-lucide-user",
  slot: "person",
} as ItemsAccordionTabs;

export const itemsTabs = [
  {
    label: "Проверки",
    icon: "i-lucide-shield-check",
    slot: "checks",
  },
  {
    label: "Полиграф",
    icon: "i-lucide-heart-pulse",
    slot: "poligrafs",
  },
  {
    label: "Расследования",
    icon: "i-lucide-hat-glasses",
    slot: "investigations",
  },
  {
    label: "Запросы",
    icon: "i-lucide-file-question-mark",
    slot: "inquiries",
  },
] as ItemsAccordionTabs[];

export const itemsAccordion = [
  {
    label: "Должности",
    icon: "i-lucide-workflow",
    slot: "staffs",
  },
  {
    label: "Образование",
    icon: "i-lucide-graduation-cap",
    slot: "educations",
  },
  {
    label: "Места работы",
    icon: "i-lucide-briefcase-business",
    slot: "workplaces",
  },
  {
    label: "Документы",
    icon: "i-lucide-book-text",
    slot: "documents",
  },
  {
    label: "Адреса",
    icon: "i-lucide-house",
    slot: "addresses",
  },
  {
    label: "Контакты",
    icon: "i-lucide-phone-call",
    slot: "contacts",
  },
  {
    label: "Изменения имени",
    icon: "i-lucide-file-pen-line",
    slot: "previous",
  },
  {
    label: "Аффилированность",
    icon: "i-lucide-users-round",
    slot: "affilations",
  },
] as ItemsAccordionTabs[];
