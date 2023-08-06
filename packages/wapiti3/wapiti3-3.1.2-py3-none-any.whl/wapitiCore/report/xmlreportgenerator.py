#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This file is part of the Wapiti project (https://wapiti-scanner.github.io)
# Copyright (C) 2008-2022 Nicolas Surribas
#
# Original authors :
# Alberto Pastor
# David del Pozo
# Copyright (C) 2008 Informatica Gesfor
# ICT Romulus (http://www.ict-romulus.eu)
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
from xml.dom.minidom import Document, Element

from wapitiCore.report.reportgenerator import ReportGenerator


class XMLReportGenerator(ReportGenerator):
    """
    This class generates a report with the method printToFile(fileName) which contains
    the information of all the vulnerabilities notified to this object through the
    method add_vulnerability(vulnerabilityTypeName,level,url,parameter,info).
    The format of the file is XML and it has the following structure:
    <report type="security">
        <generatedBy id="Wapiti X.X.X"/>
        <vulnerabilityTypeList>
            <vulnerabilityType name="SQL Injection">

        <vulnerabilityTypeList>
            <vulnerabilityType name="SQL Injection">
                <vulnerabilityList>
                    <vulnerability level="3">
                        <url>http://www.a.com</url>
                        <parameters>id=23</parameters>
                        <info>SQL Injection</info>
                    </vulnerability>
                </vulnerabilityList>
            </vulnerabilityType>
        </vulnerabilityTypeList>
    </report>
    """

    def __init__(self):
        super().__init__()
        self._xml_doc = Document()
        self._flaw_types = {}

        self._vulns = {}
        self._anomalies = {}
        self._additionals = {}

    # Vulnerabilities
    def add_vulnerability_type(self, name, description="", solution="", references=None, wstg=None):
        if name not in self._flaw_types:
            self._flaw_types[name] = {
                "desc": description,
                "sol": solution,
                "ref": references,
                "wstg": wstg
            }
        if name not in self._vulns:
            self._vulns[name] = []

    def add_vulnerability(self, module: str, category=None, level=0, request=None, parameter="", info="", wstg=None):
        """
        Store the information about the vulnerability to be printed later.
        The method printToFile(fileName) can be used to save in a file the
        vulnerabilities notified through the current method.
        """

        vuln_dict = {
            "method": request.method,
            "path": request.file_path,
            "info": info,
            "level": level,
            "parameter": parameter,
            "referer": request.referer,
            "module": module,
            "http_request": request.http_repr(left_margin=""),
            "curl_command": request.curl_repr,
            "wstg": wstg
        }

        if category not in self._vulns:
            self._vulns[category] = []
        self._vulns[category].append(vuln_dict)

    # Anomalies
    def add_anomaly_type(self, name, description="", solution="", references=None, wstg=None):
        if name not in self._flaw_types:
            self._flaw_types[name] = {
                "desc": description,
                "sol": solution,
                "ref": references,
                "wstg": wstg
            }
        if name not in self._anomalies:
            self._anomalies[name] = []

    def add_anomaly(self, module: str, category=None, level=0, request=None, parameter="", info="", wstg=None):
        """
        Store the information about the vulnerability to be printed later.
        The method printToFile(fileName) can be used to save in a file the
        vulnerabilities notified through the current method.
        """

        anom_dict = {
            "method": request.method,
            "path": request.file_path,
            "info": info,
            "level": level,
            "parameter": parameter,
            "referer": request.referer,
            "module": module,
            "http_request": request.http_repr(left_margin=""),
            "curl_command": request.curl_repr,
            "wstg": wstg
        }
        if category not in self._anomalies:
            self._anomalies[category] = []
        self._anomalies[category].append(anom_dict)

    # Additionals
    def add_additional_type(self, name, description="", solution="", references=None, wstg=None):
        """
        This method adds an addtional type, it can be invoked to include in the
        report the type.
        """
        if name not in self._flaw_types:
            self._flaw_types[name] = {
                "desc": description,
                "sol": solution,
                "ref": references,
                "wstg": wstg
            }
        if name not in self._additionals:
            self._additionals[name] = []

    def add_additional(self, module: str, category=None, level=0, request=None, parameter="", info="", wstg=None):
        """
        Store the information about the addtional to be printed later.
        The method printToFile(fileName) can be used to save in a file the
        addtionals notified through the current method.
        """

        addition_dict = {
            "method": request.method,
            "path": request.file_path,
            "info": info,
            "level": level,
            "parameter": parameter,
            "referer": request.referer,
            "module": module,
            "http_request": request.http_repr(left_margin=""),
            "curl_command": request.curl_repr,
            "wstg": wstg
        }
        if category not in self._additionals:
            self._additionals[category] = []
        self._additionals[category].append(addition_dict)

    def generate_report(self, output_path):
        """
        Create a xml file with a report of the vulnerabilities which have been logged with
        the method add_vulnerability(vulnerabilityTypeName,level,url,parameter,info)
        """

        report = self._xml_doc.createElement("report")
        report.setAttribute("type", "security")
        self._xml_doc.appendChild(report)

        # Add report infos
        report_infos = self._create_info_section()
        report.appendChild(report_infos)

        vulnerabilities = self._xml_doc.createElement("vulnerabilities")
        anomalies = self._xml_doc.createElement("anomalies")
        additionals = self._xml_doc.createElement("additionals")

        # Loop on each flaw classification
        for flaw_type_name, flaw_type in self._flaw_types.items():
            container = None
            classification = ""
            flaw_dict = {}
            if flaw_type_name in self._vulns:
                container = vulnerabilities
                classification = "vulnerability"
                flaw_dict = self._vulns
            elif flaw_type_name in self._anomalies:
                container = anomalies
                classification = "anomaly"
                flaw_dict = self._anomalies
            elif flaw_type_name in self._additionals:
                container = additionals
                classification = "additional"
                flaw_dict = self._additionals

            # Child nodes with a description of the flaw type
            flaw_type_node = self._xml_doc.createElement(classification)
            flaw_type_node.setAttribute("name", flaw_type_name)
            flaw_type_desc = self._xml_doc.createElement("description")
            flaw_type_desc.appendChild(self._xml_doc.createCDATASection(flaw_type["desc"]))
            flaw_type_node.appendChild(flaw_type_desc)
            flaw_type_solution = self._xml_doc.createElement("solution")
            flaw_type_solution.appendChild(self._xml_doc.createCDATASection(flaw_type["sol"]))
            flaw_type_node.appendChild(flaw_type_solution)

            flaw_type_references = self._xml_doc.createElement("references")
            for ref in flaw_type["ref"]:
                reference_node = self._xml_doc.createElement("reference")
                title_node = self._xml_doc.createElement("title")
                url_node = self._xml_doc.createElement("url")
                title_node.appendChild(self._xml_doc.createTextNode(ref))
                url = flaw_type["ref"][ref]
                url_node.appendChild(self._xml_doc.createTextNode(url))
                wstg_node = self._xml_doc.createElement("wstg")
                for wstg_code in flaw_type["wstg"] or []:
                    wstg_code_node = self._xml_doc.createElement("code")
                    wstg_code_node.appendChild(self._xml_doc.createTextNode(wstg_code))
                    wstg_node.appendChild(wstg_code_node)
                reference_node.appendChild(title_node)
                reference_node.appendChild(url_node)
                reference_node.appendChild(wstg_node)
                flaw_type_references.appendChild(reference_node)
            flaw_type_node.appendChild(flaw_type_references)

            # And child nodes with each flaw of the current type
            entries_node = self._xml_doc.createElement("entries")
            for flaw in flaw_dict[flaw_type_name]:
                entry_node = self._xml_doc.createElement("entry")
                method_node = self._xml_doc.createElement("method")
                method_node.appendChild(self._xml_doc.createTextNode(flaw["method"]))
                entry_node.appendChild(method_node)
                path_node = self._xml_doc.createElement("path")
                path_node.appendChild(self._xml_doc.createTextNode(flaw["path"]))
                entry_node.appendChild(path_node)
                level_node = self._xml_doc.createElement("level")
                level_node.appendChild(self._xml_doc.createTextNode(str(flaw["level"])))
                entry_node.appendChild(level_node)
                parameter_node = self._xml_doc.createElement("parameter")
                parameter_node.appendChild(self._xml_doc.createTextNode(flaw["parameter"]))
                entry_node.appendChild(parameter_node)
                info_node = self._xml_doc.createElement("info")
                info_node.appendChild(self._xml_doc.createTextNode(flaw["info"]))
                entry_node.appendChild(info_node)
                referer_node = self._xml_doc.createElement("referer")
                referer_node.appendChild(self._xml_doc.createTextNode(flaw["referer"]))
                entry_node.appendChild(referer_node)
                module_node = self._xml_doc.createElement("module")
                module_node.appendChild(self._xml_doc.createTextNode(flaw["module"]))
                entry_node.appendChild(module_node)
                http_request_node = self._xml_doc.createElement("http_request")
                http_request_node.appendChild(self._xml_doc.createCDATASection(flaw["http_request"]))
                entry_node.appendChild(http_request_node)
                curl_command_node = self._xml_doc.createElement("curl_command")
                curl_command_node.appendChild(self._xml_doc.createCDATASection(flaw["curl_command"]))
                entry_node.appendChild(curl_command_node)
                wstg_node = self._xml_doc.createElement("wstg")
                for wstg_code in flaw["wstg"] or []:
                    wstg_code_node = self._xml_doc.createElement("code")
                    wstg_code_node.appendChild(self._xml_doc.createTextNode(wstg_code))
                    wstg_node.appendChild(wstg_code_node)
                entry_node.appendChild(wstg_node)
                entries_node.appendChild(entry_node)
            flaw_type_node.appendChild(entries_node)
            container.appendChild(flaw_type_node)
        report.appendChild(vulnerabilities)
        report.appendChild(anomalies)
        report.appendChild(additionals)

        with open(output_path, "w", errors="ignore", encoding='utf-8') as xml_report_file:
            self._xml_doc.writexml(xml_report_file, addindent="   ", newl="\n")

    def _create_info_section(self) -> Element:
        """
        Write the authentication section explaining what method, fields, url were used and also if it has been
        successful
        """
        report_infos = self._xml_doc.createElement("report_infos")
        generator_name = self._xml_doc.createElement("info")
        generator_name.setAttribute("name", "generatorName")
        generator_name.appendChild(self._xml_doc.createTextNode("wapiti"))
        report_infos.appendChild(generator_name)

        generator_version = self._xml_doc.createElement("info")
        generator_version.setAttribute("name", "generatorVersion")
        generator_version.appendChild(self._xml_doc.createTextNode(self._infos["version"]))
        report_infos.appendChild(generator_version)

        scope = self._xml_doc.createElement("info")
        scope.setAttribute("name", "scope")
        scope.appendChild(self._xml_doc.createTextNode(self._infos["scope"]))
        report_infos.appendChild(scope)

        date_of_scan = self._xml_doc.createElement("info")
        date_of_scan.setAttribute("name", "dateOfScan")
        date_of_scan.appendChild(self._xml_doc.createTextNode(self._infos["date"]))
        report_infos.appendChild(date_of_scan)

        target = self._xml_doc.createElement("info")
        target.setAttribute("name", "target")
        target.appendChild(self._xml_doc.createTextNode(self._infos["target"]))
        report_infos.appendChild(target)

        target = self._xml_doc.createElement("info")
        target.setAttribute("name", "crawledPages")
        target.appendChild(self._xml_doc.createTextNode(str(self._infos["crawled_pages"])))
        report_infos.appendChild(target)

        auth_node = self._xml_doc.createElement("info")
        auth_node.setAttribute("name", "auth")

        if self._infos.get("auth") is not None:
            auth_dict = self._infos["auth"]
            is_logged_in = "true" if auth_dict["logged_in"] is True else "false"

            auth_method_node = self._xml_doc.createElement("method")
            auth_method_node.appendChild(self._xml_doc.createTextNode(auth_dict["method"]))
            auth_node.appendChild(auth_method_node)
            auth_url_node = self._xml_doc.createElement("url")
            auth_url_node.appendChild(self._xml_doc.createTextNode(auth_dict["url"]))
            auth_node.appendChild(auth_url_node)
            auth_logged_in_node = self._xml_doc.createElement("logged_in")
            auth_logged_in_node.appendChild(self._xml_doc.createTextNode(is_logged_in))
            auth_node.appendChild(auth_logged_in_node)

            form_node = self._xml_doc.createElement("form")
            if auth_dict.get("form") is not None and len(auth_dict["form"]) > 0:
                auth_form_dict = auth_dict["form"]

                form_login_field_node = self._xml_doc.createElement("login_field")
                form_login_field_node.appendChild(self._xml_doc.createTextNode(auth_form_dict["login_field"]))
                form_node.appendChild(form_login_field_node)
                form_password_field_node = self._xml_doc.createElement("password_field")
                form_password_field_node.appendChild(self._xml_doc.createTextNode(auth_form_dict["password_field"]))
                form_node.appendChild(form_password_field_node)
                auth_node.appendChild(form_node)
            else:
                form_node.setAttributeNS("http://www.w3.org/2001/XMLSchema-instance", "xsi:nil", "true")
        else:
            auth_node.setAttributeNS("http://www.w3.org/2001/XMLSchema-instance", "xsi:nil", "true")
        report_infos.appendChild(auth_node)
        return report_infos
