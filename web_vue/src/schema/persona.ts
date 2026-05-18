import { localStr, timeAgoStr } from "@/utils";
import type { FormField, ItemField, Person, TableColumns } from "@/types";

export const tableColumns: TableColumns<Person>[] = [
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

export const divsPerson = [
  { key: "surname", label: "Фамилия" },
  { key: "firstname", label: "Имя" },
  { key: "patronymic", label: "Отчество" },
  { key: "birthday", label: "Дата рождения", div: (row) => localStr(row.birthday) },
  { key: "birthplace", label: "Место рождения" },
  { key: "citizenship", label: "Гражданство" },
  { key: "dual", label: "Двойное гражданство" },
  { key: "snils", label: "СНИЛС" },
  { key: "inn", label: "ИНН" },
  { key: "marital", label: "Семейное положение" },
  { key: "created", label: "Дата записи", div: (row) => localStr(row.created) },
  { key: "addition", label: "Дополнительная информация" },
  { key: "destination", label: "Материалы проверок", slot: true },
] as ItemField<Person>[];

const pattern = "^[А-ЯЁ][А-ЯЁ\\-.,' ]+[А-ЯЁ]$";

export const formPerson = [
  {
    element: "input",
    key: "surname",
    label: "Фамилия",
    attrs: {
      pattern: pattern,
      placeholder: "Фамилия (заглавными буквами)",
      maxlength: 255,
      required: true,
    },
  },
  {
    element: "input",
    key: "firstname",
    label: "Имя",
    attrs: {
      pattern: pattern,
      placeholder: "Имя (заглавными буквами)",
      maxlength: 255,
      required: true,
    },
  },
  {
    element: "input",
    key: "patronymic",
    label: "Отчество",
    attrs: {
      pattern: pattern,
      placeholder: "Отчество (заглавными буквами)",
      maxlength: 255,
    },
  },
  {
    element: "input",
    key: "birthday",
    label: "Дата рождения",
    attrs: { type: "date", required: true },
  },
  {
    element: "input",
    key: "birthplace",
    label: "Место рождения",
    attrs: { placeholder: "Место рождения", maxlength: 255 },
  },
  {
    element: "input",
    key: "citizenship",
    label: "Гражданство",
    attrs: { placeholder: "Гражданство", maxlength: 255 },
  },
  {
    element: "input",
    key: "dual",
    label: "Двойное гражданство",
    attrs: { placeholder: "Двойное гражданство", maxlength: 255 },
  },
  {
    element: "input",
    key: "snils",
    label: "СНИЛС",
    attrs: { pattern: "^\\d{11}$", placeholder: "СНИЛС" },
  },
  {
    element: "input",
    key: "inn",
    label: "ИНН",
    attrs: { pattern: "^\\d{12}$", placeholder: "ИНН" },
  },
  {
    element: "input",
    key: "marital",
    label: "Семейное положение",
    attrs: { placeholder: "Семейное положение", maxlength: 255 },
  },
  {
    element: "textarea",
    key: "addition",
    label: "Дополнительно",
    attrs: { placeholder: "Дополнительная информация", maxlength: 4096 },
  },
] as FormField<Person>[];
